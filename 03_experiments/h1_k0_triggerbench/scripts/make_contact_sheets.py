#!/usr/bin/env python3
import csv
import pathlib
import sys
from PIL import Image, ImageDraw, ImageFont

run=pathlib.Path(sys.argv[1])
rows=list(csv.DictReader((run/'sample_manifest.csv').open(encoding='utf-8',newline='')))
out=run/'contact_sheets';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for category in sorted({r['category'] for r in rows}):
    sheet=Image.new('RGB',(1200,4*430),'white');d=ImageDraw.Draw(sheet)
    for j,r in enumerate(x for x in rows if x['category']==category):
        y=j*430
        d.text((12,y+10),r['pair_id']+' | '+category,fill='black',font=font)
        text=r['text']
        words=text.split();line='';lines=[]
        for w in words:
            candidate=(line+' '+w).strip()
            if d.textlength(candidate,font=font)>1160 and line:lines.append(line);line=w
            else:line=candidate
        if line:lines.append(line)
        for k,s in enumerate(lines[:4]):d.text((12,y+39+k*22),s,fill='black',font=font)
        for side,x in [('safe',12),('unsafe',612)]:
            path=r[f'{side}_local_path']
            if path and pathlib.Path(path).exists():
                with Image.open(path) as im:
                    im=im.convert('RGB');im.thumbnail((570,300))
                    sheet.paste(im,(x+(570-im.width)//2,y+120+(300-im.height)//2))
            else:d.text((x+50,y+220),'DOWNLOAD FAILED',fill='red',font=font)
            d.text((x,y+100),side.upper(),fill='black',font=font)
    sheet.save(out/f'{category}.jpg',quality=88)
print(len(list(out.glob('*.jpg'))))
