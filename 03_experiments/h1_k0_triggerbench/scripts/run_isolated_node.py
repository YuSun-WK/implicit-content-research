"""Run an owned isolated proxy and one bounded child; clean up both on exit."""
import os,sys,json,pathlib,subprocess,tempfile,signal,time
root=pathlib.Path(__file__).resolve().parents[1];run=root/'runs/h1_singbox_20261116_082046';nodes=[x for x in json.load(open('/etc/sing-box/config.json'))['outbounds'] if x['type'] not in ('direct','urltest','selector','block','dns')]
port=int(os.environ.get('H1_PORT','17900'));index=int(os.environ.get('H1_NODE','10'))-1
child=None;proxy=None
def stop(*_):raise KeyboardInterrupt()
signal.signal(signal.SIGTERM,stop)
try:
 with tempfile.TemporaryDirectory(prefix='owned-proxy-',dir=run) as d:
  p=pathlib.Path(d);os.chmod(p,0o700);node=dict(nodes[index]);node['tag']='candidate';config={'log':{'disabled':True},'inbounds':[{'type':'mixed','listen':'127.0.0.1','listen_port':port}],'outbounds':[node],'route':{'final':'candidate','auto_detect_interface':True}}
  path=p/'config.json';path.write_text(json.dumps(config));os.chmod(path,0o600)
  proxy=subprocess.Popen(['sing-box','run','-c',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
  if proxy.poll() is not None:raise RuntimeError('proxy start failed')
  env=os.environ.copy()
  for k in ['http_proxy','https_proxy','all_proxy','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY']:env[k]=f'http://127.0.0.1:{port}'
  child=subprocess.Popen(sys.argv[1:],env=env);code=child.wait();sys.exit(code)
finally:
 for proc in [child,proxy]:
  if proc and proc.poll() is None:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
