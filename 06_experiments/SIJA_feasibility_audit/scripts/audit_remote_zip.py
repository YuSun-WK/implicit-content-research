import urllib.request,struct,json,io,zipfile,zlib
url='https://huggingface.co/datasets/xianminye/SI2ESBench/resolve/4087764c55ea76946bac6634aa4d63b2ad7bb5a0/SI2ESBench.zip'
def get(a,b):
 r=urllib.request.urlopen(urllib.request.Request(url+'?range_start='+str(a),headers={'Range':f'bytes={a}-{b}'}),timeout=45)
 if r.status!=206: raise RuntimeError('Range unsupported: '+str(r.status))
 return r.read(b-a+2)
n=1003437789;tail=get(n-65536,n-1);i=tail.rfind(b'PK\x05\x06');e=struct.unpack_from('<4s4H2LH',tail,i);size,off=e[5:7];cd=get(off,off+size-1);z=zipfile.ZipFile(io.BytesIO(cd+struct.pack('<4s4H2LH',b'PK\x05\x06',0,0,e[3],e[4],size,0,0)))
entries=[{'name':x.filename,'size':x.file_size,'compressed':x.compress_size,'offset':x.header_offset,'crc':x.CRC} for x in z.infolist()];json.dump(entries,open('/tmp/zipentries.json','w'));print('entries',len(entries));print([x for x in entries if x['name'].endswith(('.json','.csv','.txt','.jsonl'))])
for x in entries:
 if x['name'].endswith(('.json','.csv','.jsonl')) and x['size']<5000000:
  h=get(x['offset'],x['offset']+29);v=struct.unpack('<4s5H3L2H',h);start=x['offset']+30+v[-2]+v[-1];data=get(start,start+x['compressed']-1);data=zlib.decompress(data,-15) if v[3]==8 else data;open('/tmp/dataset_metadata'+('.json' if x['name'].endswith('.json') else '.txt'),'wb').write(data);print('metadata extracted',len(data))
