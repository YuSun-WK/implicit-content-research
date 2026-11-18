"""Serve only one anonymous bundle on loopback; no repository/private directory listing."""
import argparse,http.server,pathlib,re,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Handler(http.server.SimpleHTTPRequestHandler):
 def do_GET(self):
  path=urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
  if path=='/':path='/index.html'
  allowed={'/index.html','/app.js','/style.css','/materials.js','/GUIDE.md','/review_form_stage1.csv','/review_form_stage2.csv'}
  if path not in allowed and not re.fullmatch('/assets/[a-f0-9]{20}\\.png',path):self.send_error(404);return
  candidate=(pathlib.Path(self.directory)/path.lstrip('/')).resolve()
  if not candidate.is_relative_to(pathlib.Path(self.directory).resolve()):self.send_error(404);return
  self.path=path;super().do_GET()
 def do_HEAD(self):self.send_error(405)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--reviewer',choices=['ReviewerA','ReviewerB'],required=True);p.add_argument('--port',type=int,default=8765);a=p.parse_args();directory=ROOT/'packages'/a.reviewer
 if not (directory/'index.html').is_file():raise SystemExit('Build review package first')
 handler=lambda *args,**kwargs:Handler(*args,directory=str(directory),**kwargs)
 with http.server.ThreadingHTTPServer(('127.0.0.1',a.port),handler) as server:
  print(f'Only anonymous {a.reviewer} served at http://127.0.0.1:{server.server_port}/',flush=True);server.serve_forever()
