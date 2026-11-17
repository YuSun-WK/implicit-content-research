"""Rebuild the exploratory 2-ID pilot manifest; metadata text remains private."""
import json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--metadata',required=True);p.add_argument('--data-dir',required=True);p.add_argument('--output',required=True);a=p.parse_args()
config=Path(__file__).parents[1]/'configs';prompts=json.loads((config/'prompts.json').read_text());rows=[]
metadata={x['id']:x for x in json.loads(Path(a.metadata).read_text())}
for ident in [329,310]:
    x=metadata[ident]
    for condition in ['natural','draft-intent','matched','direct','strong']:
        row=dict(id=f'SIJA-{ident}',condition=condition,images=[str(Path(a.data_dir)/x['image-path']),str(Path(a.data_dir)/f'cue_images/{ident}.png')],text=x['prompt'])
        if condition=='draft-intent':row.update(referent=x['prompt'],action=x['action'],specification=x['spec-annotation'])
        if condition=='matched':row['neutral_context']=json.dumps(dict(referent='Refer to the original source image and user text; no additional object annotation is supplied.',action='Refer to the original visual cue; no additional operation annotation is supplied.',specification='Refer to the original visual cue; no additional result annotation is supplied.'))
        if condition in ['direct','strong']:row['system']=prompts[condition]
        rows.append(row)
Path(a.output).write_text(json.dumps(rows))
