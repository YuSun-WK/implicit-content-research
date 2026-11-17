"""Explicit fixed-revision download into caller-owned cache. Never loads GPUs."""
import argparse,json
from pathlib import Path
from huggingface_hub import HfApi,snapshot_download
p=argparse.ArgumentParser();p.add_argument('--cache-dir',required=True);args=p.parse_args()
rev='ebb281ec70b05090aa6165b016eac8ec08e71b17';repo='Qwen/Qwen3-VL-4B-Instruct'
info=HfApi().model_info(repo,revision=rev,files_metadata=True)
assert info.sha==rev
print('Estimated download bytes',sum(f.size or 0 for f in info.siblings),flush=True)
path=snapshot_download(repo,revision=rev,cache_dir=args.cache_dir,allow_patterns=['*.json','*.txt','*.safetensors'],max_workers=2)
index=json.loads((Path(path)/'model.safetensors.index.json').read_text())
for f in set(index['weight_map'].values()):
    actual=Path(path)/f;expected=next(x.size for x in info.siblings if x.rfilename==f)
    assert actual.stat().st_size==expected
print('All indexed weight files complete by declared size:',path)
