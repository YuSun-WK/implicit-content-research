"""Read permitted sing-box config; isolate node probes; never print credentials."""
import json,pathlib,subprocess,tempfile,os,time,requests,socket,signal,hashlib,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1];RUN=ROOT/'runs/h1_singbox_20261116_082046';RUN.mkdir(exist_ok=True)
CONFIG='/etc/sing-box/config.json';c=json.load(open(CONFIG));nodes=[x for x in c['outbounds'] if x['type'] not in ('direct','urltest','selector','block','dns')]
def alarm(*_):raise TimeoutError('node wall time limit')
signal.signal(signal.SIGALRM,alarm)
for idx,node in enumerate(nodes,1):
 rec={'node':f'N{idx:02d}','type':node['type'],'tests':[],'started':time.time()};proc=None
 try:
  signal.alarm(110)
  with tempfile.TemporaryDirectory(prefix='h1-node-',dir=RUN) as d:
   p=pathlib.Path(d);os.chmod(p,0o700);out=dict(node);out['tag']='candidate'
   conf={'log':{'disabled':True},'inbounds':[{'type':'mixed','listen':'127.0.0.1','listen_port':17898}], 'outbounds':[out], 'route':{'final':'candidate','auto_detect_interface':True}}
   path=p/'config.json';path.write_text(json.dumps(conf));os.chmod(path,0o600)
   proc=subprocess.Popen(['sing-box','run','-c',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   for _ in range(30):
    if proc.poll() is not None:raise RuntimeError('isolated instance failed')
    try:
     sock=socket.create_connection(('127.0.0.1',17898),.1);sock.close();break
    except OSError:time.sleep(.1)
   session=requests.Session();session.trust_env=False;session.proxies={'http':'http://127.0.0.1:17898','https':'http://127.0.0.1:17898'}
   for n in [1048576,16777216,16777216]:
    t=time.monotonic();r=None;test={'requested_bytes':n}
    try:
     url='https://huggingface.co/Sandy124/ThinkingGuard-8B/resolve/76892f9768ce828268265171f4bbc5dfb75eafc3/model-00001-of-00004.safetensors?nodeprobe='+str(time.time_ns())
     r=session.get(url,headers={'Range':f'bytes=268435456-{268435456+n-1}'},stream=True,timeout=(8,20))
     test.update(status=r.status_code,download_host=urllib.parse.urlsplit(r.url).hostname,content_range=r.headers.get('Content-Range'))
     if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes 268435456-{268435456+n-1}/4905357176':raise ValueError('invalid Range response')
     count=0;h=hashlib.sha256()
     for chunk in r.iter_content(1048576):count+=len(chunk);h.update(chunk)
     if count!=n:raise ValueError('byte count mismatch')
     test.update(ok=True,bytes=count,sha256=h.hexdigest())
    except Exception as e:test.update(ok=False,error_type=type(e).__name__)
    finally:
     if r is not None:r.close()
     test['seconds']=time.monotonic()-t;rec['tests'].append(test)
    if not test['ok']:break
   session.close()
 except Exception as e:rec['error_type']=type(e).__name__
 finally:
  signal.alarm(0)
  if proc is not None:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
  rec['ended']=time.time()
  with (RUN/'node_tests.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
  print(json.dumps(rec),flush=True)
