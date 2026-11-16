import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from safetensors.numpy import save_file
from scripts.audit_model_cache import REVISIONS, REQUIRED, SHARDS, inspect_snapshot, sha256_file
from unittest.mock import patch

MODEL = 'Sandy124/ThinkingGuard-8B'
REV = REVISIONS[MODEL]


class CacheAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/REV
        self.path.mkdir()
        for name in REQUIRED[MODEL]:
            (self.path/name).write_text('{}')
        (self.path/'config.json').write_text(json.dumps({
            'architectures': ['Qwen3VLForConditionalGeneration'], 'model_type': 'qwen3_vl'}))
        self.shard = self.path/'model-00001-of-00001.safetensors'
        save_file({'weight': np.array([1.0], dtype=np.float32)}, str(self.shard))
        self.shards_patch = patch.dict(SHARDS, {MODEL: {self.shard.name: (self.shard.stat().st_size, sha256_file(self.shard))}})
        self.shards_patch.start()
        self.addCleanup(self.shards_patch.stop)
        (self.path/'model.safetensors.index.json').write_text(json.dumps({
            'weight_map': {'weight': self.shard.name}, 'metadata': {'total_size': 4}}))

    def test_complete_header(self):
        self.assertTrue(inspect_snapshot(self.path, MODEL, REV)['ready'])

    def test_missing_shard(self):
        self.shard.unlink()
        result = inspect_snapshot(self.path, MODEL, REV)
        self.assertFalse(result['ready'])
        self.assertIn(self.shard.name, result['missing'])

    def test_corrupt_shard(self):
        self.shard.write_bytes(b'not safetensors')
        result = inspect_snapshot(self.path, MODEL, REV)
        self.assertFalse(result['ready'])
        self.assertTrue(result['invalid'])

    def test_same_size_hash_mismatch(self):
        data = bytearray(self.shard.read_bytes())
        data[-1] ^= 1
        self.shard.write_bytes(data)
        result = inspect_snapshot(self.path, MODEL, REV)
        self.assertFalse(result['ready'])
        self.assertTrue(any('SHA256 mismatch' in value for value in result['invalid']))

    def test_wrong_revision(self):
        self.assertFalse(inspect_snapshot(self.path, MODEL, 'other')['ready'])


if __name__ == '__main__':
    unittest.main()
