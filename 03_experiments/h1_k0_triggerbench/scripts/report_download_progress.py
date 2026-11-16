"""Read-only receipt rehash and pinned model audit while downloader may run."""
import pathlib,json,hashlib,datetime,time,os
from audit_model_cache import SHARDS,REVISIONS,inspect_snapshot
R=pathlib.Path(__file__).resolve().parents[1];run=R/'runs/h1_singbox_20261116_082046';model='Sandy124/ThinkingGuard-8B';snap=R/'model_snapshots/Sandy124__ThinkingGuard-8B'/REVISIONS[model];block=16*1024*1024
result={'snapshot_started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'shards':[]}
for name,(size,digest) in SHARDS[model].items():
 d=snap/(name+'.blocks16');total=(size+block-1)//block;valid=[];invalid=[]
 # Capture receipt names once; later blocks belong to a future snapshot.
 for p in list(d.glob('*.json')) if d.exists() else []:
  i=int(p.stem);f=d/str(i)
  try:
   receipt=json.loads(p.read_text());data=f.read_bytes()
   if len(data)!=min(block,size-i*block) or hashlib.sha256(data).hexdigest()!=receipt['sha256']:raise ValueError('invalid receipt block')
   valid.append(i)
  except (OSError,ValueError,KeyError):invalid.append(i)
 missing=sorted(set(range(total))-set(valid));dest=snap/name
 result['shards'].append(dict(file=name,expected_bytes=size,official_sha256=digest,expected_blocks=total,valid_blocks=len(valid),verified_block_bytes=sum(min(block,size-i*block) for i in valid),missing_blocks=missing,invalid_blocks=invalid,complete_file_exists=dest.is_file(),assembly_status='INCOMPLETE_BLOCK_SET' if missing else 'COMPLETE_SET; defer assembly to active downloader to avoid concurrent writes'))
result['audit']=inspect_snapshot(snap,model,REVISIONS[model]);log=run/'download.jsonl';events=[json.loads(l) for l in log.read_text().splitlines()];now=time.time();recent=[e for e in events if e['time']>=now-300];result.update(snapshot_ended=datetime.datetime.now(datetime.timezone.utc).isoformat(),downloader_pid108368_exists=pathlib.Path('/proc/108368').exists(),log_mtime_utc=datetime.datetime.fromtimestamp(log.stat().st_mtime,datetime.timezone.utc).isoformat(),last_event=events[-1],recent_5min_success=sum(e['event']=='block' for e in recent),recent_5min_errors=sum(e['event']=='error' for e in recent),model_loaded=False,smoke_test='NOT_RUN',formal_experiment='NOT_RUN')
(run/'latest_progress.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='audit'},indent=2))
