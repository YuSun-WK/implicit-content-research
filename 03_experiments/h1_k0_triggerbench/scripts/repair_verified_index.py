"""Repair only shard locations after pinned SHA verification and exact tensor-set validation."""
import pathlib,json,hashlib,math,shutil
from safetensors import safe_open
from audit_model_cache import SHARDS,REVISIONS,sha256_file
MODEL='Sandy124/ThinkingGuard-8B'
def repair(root):
 root=pathlib.Path(root)
 if root.name!=REVISIONS[MODEL]:raise ValueError('revision mismatch')
 index=root/'model.safetensors.index.json';original=root/'model.safetensors.index.official.json'
 source=original if original.exists() else index;raw=source.read_bytes();old=json.loads(raw)
 metadata=json.loads((root/'official_metadata.json').read_text())
 if metadata['sha']!=REVISIONS[MODEL]:raise ValueError('official metadata revision mismatch')
 entry=next(e for e in metadata['siblings'] if e['rfilename']==index.name)
 if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=entry['blobId']:raise ValueError('official index blob mismatch')
 mapping={};total=0;sizes={'F64':8,'F32':4,'F16':2,'BF16':2,'I64':8,'I32':4,'I16':2,'I8':1,'U8':1,'BOOL':1}
 for name,(size,digest) in SHARDS[MODEL].items():
  p=root/name
  if p.stat().st_size!=size or sha256_file(p)!=digest:raise ValueError('pinned shard integrity failed')
  with p.open('rb') as stream:n=int.from_bytes(stream.read(8),'little');head=json.loads(stream.read(n))
  offsets=[]
  with safe_open(p,framework='pt',device='cpu') as f:
   for k in f.keys():
    if k in mapping:raise ValueError('duplicate tensor')
    v=head[k];a,b=v['data_offsets']
    if list(f.get_slice(k).get_shape())!=v['shape'] or b-a!=math.prod(v['shape'])*sizes[v['dtype']]:raise ValueError('shape/byte mismatch')
    mapping[k]=name;offsets.append((a,b));total+=b-a
  cursor=0
  for a,b in sorted(offsets):
   if a!=cursor:raise ValueError('offset gap/overlap')
   cursor=b
  if cursor!=size-8-n:raise ValueError('data length mismatch')
 if set(mapping)!=set(old['weight_map']) or total!=old['metadata']['total_size']:raise ValueError('global tensor set/size mismatch')
 fixed=dict(old,weight_map=dict(sorted(mapping.items())));data=(json.dumps(fixed,indent=2)+'\n').encode()
 if not original.exists():shutil.copyfile(index,original)
 temp=root/'model.safetensors.index.repaired.tmp';temp.write_bytes(data);temp.replace(index)
 provenance=dict(model=MODEL,revision=REVISIONS[MODEL],weight_bytes_unchanged=True,tensors=len(mapping),total_tensor_bytes=total,changed_locations=sum(mapping[k]!=v for k,v in old['weight_map'].items()),official_index_sha256=hashlib.sha256(raw).hexdigest(),local_index_sha256=hashlib.sha256(data).hexdigest(),official_index_git_blob=entry['blobId'],reason='official weight_map names 118 tensor locations in different shards from the pinned official weight files')
 (root/'local_index_provenance.json').write_text(json.dumps(provenance,indent=2));return provenance
if __name__=='__main__':
 import sys
 print(json.dumps(repair(sys.argv[1]),indent=2))
