"""CPU loopback test: public-bundle root only; server always shut down."""
import functools,hashlib,http.server,pathlib,sys,threading,unittest,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from serve_review import Handler
class ServeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=ROOT/'packages/ReviewerA';cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(cls.root)));cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.base=f'http://127.0.0.1:{cls.server.server_port}';cls.client=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=3)
 def test_page_and_original_image_access(self):
  with self.client.open(self.base+'/') as r:self.assertEqual(r.status,200);self.assertIn(b'connect-src',r.read())
  image=next((self.root/'assets').glob('*.png'))
  with self.client.open(self.base+'/assets/'+image.name) as r:self.assertEqual(hashlib.sha256(r.read()).hexdigest(),hashlib.sha256(image.read_bytes()).hexdigest())
 def test_private_repo_and_traversal_denied(self):
  for path in ['/private/registry.json','/../private/seeds.json','/%2e%2e/private/registry.json','/.git/config','/answers.json','/assets/']:
   with self.assertRaises(urllib.error.HTTPError) as e:self.client.open(self.base+path)
   self.assertEqual(e.exception.code,404)
if __name__=='__main__':unittest.main()
