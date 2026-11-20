# One action on a stable authorized download machine

Run **one** of these official download routes. Use a private directory with at least 20 GiB free. The HF route pins the exact revision and is preferred.

## Linux: official Hugging Face

```bash
python3 -m venv /private/vlsu-download-venv
/private/vlsu-download-venv/bin/pip install -U huggingface_hub
REV=cc594898137f460bfe9f0759e9844b3ce807cfb5
/private/vlsu-download-venv/bin/hf download Qwen/Qwen2.5-VL-7B-Instruct \
  --revision "$REV" --include '*.safetensors' --cache-dir /private/vlsu-hf --max-workers 1
SNAP=/private/vlsu-hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$REV
```

## Linux: Qwen official ModelScope

```bash
python3 -m venv /private/vlsu-download-venv
/private/vlsu-download-venv/bin/pip install -U modelscope
/private/vlsu-download-venv/bin/python - <<'PY'
from modelscope import snapshot_download
print(snapshot_download('Qwen/Qwen2.5-VL-7B-Instruct', cache_dir='/private/vlsu-modelscope'))
PY
SNAP=/private/vlsu-modelscope/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master
```

Set `SNAP` to the actual path printed by ModelScope if different. ModelScope's default branch must pass all five HF hashes; do not transfer a mismatch. Copy `configs/stage2_model_files.json` from the GitHub branch to the download machine as `/private/stage2_model_files.json`, then verify:

```bash
python3 - "$SNAP" /private/stage2_model_files.json <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]); manifest=json.loads(pathlib.Path(sys.argv[2]).read_text()); count=0
for name,meta in manifest['files'].items():
    if not name.endswith('.safetensors'): continue
    p=root/name; h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
    ok=p.stat().st_size==meta['size'] and h.hexdigest()==meta['sha256']
    print(name,'PASS' if ok else 'FAIL',p.stat().st_size)
    count+=ok
if count!=5: raise SystemExit('STOP: fewer than 5 verified shards')
PY
```

Only after **5 PASS**, transfer the five files to the experiment server's existing revision named private directory. Supply your own authorized username, hostname and server path; do not upload to GitHub:

```bash
REV=cc594898137f460bfe9f0759e9844b3ce807cfb5
rsync -avP "$SNAP"/model-*.safetensors \
  user@authorized-server:/home/ubuntu/data/project/vlsu-original-repro/06_experiments/repro_vlsu_original/.local/stage2/hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$REV/
```

On Windows, create a Python virtual environment, `pip install huggingface_hub` or `pip install modelscope`, run the same `hf download` command or `snapshot_download` Python call with a private Windows cache directory, and run the verification Python block above with Windows paths. Transfer verified files using Windows OpenSSH `scp` or an authorized SFTP client. Reverify five SHA-256 values on the server before model loading. The server already holds the pinned HF metadata and the frozen images.

After transfer, Codex will run the existing `scripts/stage2_qwen_smoke.py` with the pinned CSV and Stage 1 snapshot, first Direct10 then paired Binary5 and CoT5, subject to GPU availability and the 20 GiB allocation limit.
