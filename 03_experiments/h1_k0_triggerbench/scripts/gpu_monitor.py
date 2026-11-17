"""Namespace-aware process accounting; explicit null when unavailable; device upper-bound guard."""
import os,pathlib,subprocess,time

def query_processes(gpu):
 p=subprocess.run(['nvidia-smi','--query-compute-apps=pid,used_gpu_memory','--format=csv,noheader,nounits','-i',str(gpu)],capture_output=True,text=True,timeout=5,check=True)
 result={}
 for line in p.stdout.splitlines():
  fields=[x.strip() for x in line.split(',')]
  if len(fields)==2 and fields[0].isdigit() and fields[1].isdigit():result[int(fields[0])]=int(fields[1])
 return result

def namespace_pids():
 ids={os.getpid()}
 try:
  for line in pathlib.Path('/proc/self/status').read_text().splitlines():
   if line.startswith('NSpid:'):ids.update(map(int,line.split()[1:]))
 except OSError:pass
 return ids

def process_gpu_mib(gpu,host_pid=None):
 rows=query_processes(gpu);ids={host_pid} if host_pid is not None else namespace_pids();values=[rows[p] for p in ids if p in rows]
 return sum(values) if values else None

def device_used_mib(gpu):
 p=subprocess.run(['nvidia-smi','--query-gpu=memory.used','--format=csv,noheader,nounits','-i',str(gpu)],capture_output=True,text=True,timeout=5,check=True)
 return int(p.stdout.strip())

def identify_host_pid(torch,gpu,baseline):
 """Bind a unique new NVML PID via a reversible 64MiB allocation challenge."""
 before=query_processes(gpu);new=set(before)-set(baseline)
 info={'namespace_pids':sorted(namespace_pids()),'host_pid':None,'method':'unavailable','baseline_process_count':len(baseline)}
 if len(new)!=1:return info
 candidate=next(iter(new));probe=torch.empty(64*1024*1024,dtype=torch.uint8,device='cuda:0');torch.cuda.synchronize();time.sleep(1);during=query_processes(gpu);del probe;torch.cuda.empty_cache();torch.cuda.synchronize();time.sleep(1);after=query_processes(gpu)
 info['challenge_mib']={'before':before.get(candidate),'during':during.get(candidate),'after':after.get(candidate)}
 if candidate in during and candidate in after and 48<=during[candidate]-before[candidate]<=80 and 48<=during[candidate]-after[candidate]<=80:
  info.update(host_pid=candidate,method='unique_new_pid_and_reversible_64MiB_allocation')
 elif candidate in namespace_pids():info.update(host_pid=candidate,method='namespace_pid_direct')
 return info
