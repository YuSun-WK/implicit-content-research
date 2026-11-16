#!/usr/bin/env python3
"""Read-only CPU inspection of a pinned local model snapshot; never loads weights."""
import argparse
import hashlib
import json
import pathlib

REVISIONS = {
    'Sandy124/ThinkingGuard-8B': '76892f9768ce828268265171f4bbc5dfb75eafc3',
    'Qwen/Qwen3-VL-8B-Instruct': '0c351dd01ed87e9c1b53cbc748cba10e6187ff3b',
}
REQUIRED = {
    'Sandy124/ThinkingGuard-8B': ('config.json', 'processor_config.json', 'chat_template.jinja',
                                  'tokenizer.json', 'tokenizer_config.json', 'generation_config.json', 'model.safetensors.index.json'),
    'Qwen/Qwen3-VL-8B-Instruct': ('config.json', 'preprocessor_config.json', 'video_preprocessor_config.json',
                                 'chat_template.json', 'tokenizer.json', 'tokenizer_config.json',
                                 'merges.txt', 'vocab.json', 'generation_config.json', 'model.safetensors.index.json'),
}

# Official Hugging Face LFS SHA256 and byte lengths for the fixed revisions.
SHARDS = {
    'Sandy124/ThinkingGuard-8B': {
        'model-00001-of-00004.safetensors': (4905357176, '32eea4896bf5cb65467ea1d20d7441dea603329f9354e5253a8c52211757f947'),
        'model-00002-of-00004.safetensors': (4915962456, 'b40d5eaf9ca25a5ce6bcf9f1c73cd954d417b4baffcfc6315f7962bc8e7ff26b'),
        'model-00003-of-00004.safetensors': (4974674312, '18892b0bc15ebd51ec02248d52b621a1b66fb98d81f14f4318799badda84f777'),
        'model-00004-of-00004.safetensors': (2738345504, 'bf0f4158d688cfa9498e64ae473794e6c86618328b566fff6f232cd5d3976b77'),
    },
    'Qwen/Qwen3-VL-8B-Instruct': {
        'model-00001-of-00004.safetensors': (4902275944, 'd5d0aef0eb170fc7453a296c43c0849a56f510555d3588e4fd662bb35490aefa'),
        'model-00002-of-00004.safetensors': (4915962496, '8be88fb5501e4d5719a6d4cc212e6a13480330e74f3e8c77daa1a68f199106b5'),
        'model-00003-of-00004.safetensors': (4999831048, '83de00eafe6e0d57ccd009dbcf71c9974d74df2f016c27afb7e95aafd16b2192'),
        'model-00004-of-00004.safetensors': (2716270024, '0a88b98e9f96270973f567e6a2c103ede6ccdf915ca3075e21c755604d0377a5'),
    },
}


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_safetensors_header(path, expected_keys):
    """Validate header offsets without loading tensors or importing PyTorch."""
    with path.open('rb') as stream:
        header_size = int.from_bytes(stream.read(8), 'little')
        if not 0 < header_size <= 100 * 1024 * 1024 or 8 + header_size > path.stat().st_size:
            raise ValueError('invalid header length')
        header = json.loads(stream.read(header_size))
    data_size = path.stat().st_size - 8 - header_size
    if not expected_keys or not expected_keys.issubset(header):
        raise ValueError('index tensors missing from shard header')
    for key in expected_keys:
        offsets = header[key]['data_offsets']
        if len(offsets) != 2 or not 0 <= offsets[0] <= offsets[1] <= data_size:
            raise ValueError('invalid tensor offset')


def inspect_snapshot(path, model_id, revision):
    """Check required files and safetensors headers without GPU allocation."""
    path = pathlib.Path(path)
    result = {'model_id': model_id, 'revision': revision, 'path': str(path),
              'missing': [], 'invalid': [], 'partial': [], 'shards': [], 'ready': False,
              'integrity': 'fixed-revision LFS size and SHA256 plus safetensors headers'}
    if model_id not in REVISIONS or REVISIONS[model_id] != revision:
        result['invalid'].append('unrecognized model/revision')
        return result
    if path.name != revision:
        result['invalid'].append('snapshot directory does not match fixed revision')
    for name in REQUIRED[model_id]:
        if not (path/name).is_file():
            result['missing'].append(name)
    config = path/'config.json'
    if config.is_file():
        try:
            data = json.loads(config.read_text())
            if data.get('architectures') != ['Qwen3VLForConditionalGeneration'] or data.get('model_type') != 'qwen3_vl':
                result['invalid'].append('config architecture mismatch')
        except (OSError, ValueError):
            result['invalid'].append('config.json unreadable or malformed')
    index = path/'model.safetensors.index.json'
    if index.is_file():
        try:
            data = json.loads(index.read_text())
            shards = sorted(set(data['weight_map'].values()))
            if set(shards) != set(SHARDS[model_id]):
                raise ValueError('index shard list differs from pinned revision')
            result['shards'] = shards
            for name in shards:
                shard = path/name
                if not shard.is_file():
                    result['missing'].append(name)
                    continue
                try:
                    expected_keys = {key for key, location in data['weight_map'].items() if location == name}
                    check_safetensors_header(shard, expected_keys)
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    result['invalid'].append(f'{name}: {type(exc).__name__}')
        except (OSError, ValueError, KeyError, TypeError):
            result['invalid'].append('model.safetensors.index.json unreadable or malformed')
    for name, (expected_size, expected_hash) in SHARDS[model_id].items():
        shard = path/name
        if not shard.is_file():
            if name not in result['missing']:
                result['missing'].append(name)
            continue
        if shard.stat().st_size != expected_size:
            result['invalid'].append(f'{name}: byte length mismatch')
        elif sha256_file(shard) != expected_hash:
            result['invalid'].append(f'{name}: SHA256 mismatch')
    for partial in path.glob('*.incomplete'):
        result['partial'].append(partial.name)
    result['ready'] = not (result['missing'] or result['invalid']) and bool(result['shards'])
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('model_id', choices=tuple(REVISIONS))
    ap.add_argument('model_path', type=pathlib.Path)
    args = ap.parse_args()
    result = inspect_snapshot(args.model_path, args.model_id, REVISIONS[args.model_id])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ready'] else 2)
