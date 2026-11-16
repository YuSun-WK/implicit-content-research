#!/usr/bin/env python3
"""Generate contact sheets from validated frozen image bytes."""
import argparse
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
try:
    from scripts.image_utils import load_image
except ModuleNotFoundError:
    from image_utils import load_image


def make_sheets(run, image_root, output_dir=None):
    with (run/'sample_manifest.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    # Complete validation before writing any output.
    images = {(r['pair_id'], side): load_image(r, side, image_root)
              for r in rows for side in ('safe', 'unsafe')}
    out = output_dir or run/'contact_sheets'
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    for category in sorted({r['category'] for r in rows}):
        category_rows = [r for r in rows if r['category'] == category]
        sheet = Image.new('RGB', (1200, len(category_rows)*430), 'white')
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(category_rows):
            y = j*430
            draw.text((12, y+10), row['pair_id']+' | '+category, fill='black', font=font)
            line = ''; lines = []
            for word in row['text'].split():
                candidate = (line+' '+word).strip()
                if draw.textlength(candidate, font=font) > 1160 and line:
                    lines.append(line); line = word
                else:
                    line = candidate
            if line:
                lines.append(line)
            for k, value in enumerate(lines[:4]):
                draw.text((12, y+39+k*22), value, fill='black', font=font)
            for side, x in (('safe', 12), ('unsafe', 612)):
                im = images[(row['pair_id'], side)].copy()
                im.thumbnail((570, 300))
                sheet.paste(im, (x+(570-im.width)//2, y+120+(300-im.height)//2))
                draw.text((x, y+100), side.upper(), fill='black', font=font)
        sheet.save(out/f'{category}.jpg', quality=88)
    return len(list(out.glob('*.jpg')))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('run', type=Path)
    ap.add_argument('--image-root', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path)
    args = ap.parse_args()
    print(make_sheets(args.run, args.image_root, args.output_dir))
