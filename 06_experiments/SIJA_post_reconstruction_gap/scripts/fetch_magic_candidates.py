"""Refresh expiring viewer image URLs; save privately. Revision query is not proof of byte pinning."""
import argparse,json,urllib.request,hashlib,io
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--private-dir',required=True);a=p.parse_args();dest=Path(a.private_dir);dest.mkdir(exist_ok=True,parents=True);out=[]
for index in [16,20,13,21]:
    r={'row_idx':index,'review_status':'PENDING','safety_label':'UNVERIFIED','format':'NO_MATCHED_CUE'}
    try:
        u=f'https://datasets-server.huggingface.co/rows?dataset=osunlp%2FMagicBrush&config=default&split=dev&offset={index}&length=1&revision=6c254560879df7851233ea0fd2ae2a62764d0ef2'
        record=json.load(urllib.request.urlopen(u,timeout=15))['rows'][0];raw=urllib.request.urlopen(record['row']['source_img']['src'],timeout=15).read();im=Image.open(io.BytesIO(raw));im.load();(dest/f'magic-{index}.image').write_bytes(raw);(dest/f'magic-{index}.json').write_text(json.dumps(record));r.update(decode=True,sha256=hashlib.sha256(raw).hexdigest(),size=list(im.size))
    except Exception as e:r.update(decode=False,error_type=type(e).__name__)
    out.append(r)
(dest/'fresh_decode.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
