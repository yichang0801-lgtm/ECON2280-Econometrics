"""Render the exact delivered PDF and make numbered four-page review sheets."""
from pathlib import Path
import json
import hashlib
import re
import fitz
from PIL import Image,ImageOps,ImageDraw

ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'qa'/'rendered';out.mkdir(exist_ok=True)
    pdf=ROOT/'Econometrics中文版笔记.pdf';doc=fitz.open(pdf)
    old_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('page-*.png')}
    changed=[]
    tiles=[]
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=fitz.Matrix(1.65,1.65),alpha=False)
        img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        image_path=out/f'page-{i+1:02}.png'
        img.save(image_path)
        if old_hashes.get(image_path.name)!=hashlib.sha256(image_path.read_bytes()).hexdigest():changed.append(i+1)
        tile=Image.new('RGB',(1000,1450),'#e8e8e8')
        thumb=ImageOps.contain(img,(980,1400))
        tile.paste(thumb,((1000-thumb.width)//2,35))
        ImageDraw.Draw(tile).text((12,10),f'PDF page {i+1} / {len(doc)}',fill='black')
        tiles.append(tile)
    sheets=[]
    for start in range(0,len(tiles),4):
        batch=tiles[start:start+4];sheet=Image.new('RGB',(2000,1450*((len(batch)+1)//2)),'white')
        for k,tile in enumerate(batch):sheet.paste(tile,((k%2)*1000,(k//2)*1450))
        p=out/f'sheet-{start//4+1:02}.png';sheet.save(p);sheets.append(p.relative_to(ROOT).as_posix())
    # Remove only obsolete renderer-owned PNGs inside this exact output folder.
    for p in out.glob('*.png'):
        match=re.fullmatch(r'(page|sheet)-(\d+)\.png',p.name)
        if match and int(match[2])>(len(doc) if match[1]=='page' else len(sheets)):
            assert p.resolve().parent==out.resolve()
            p.unlink()
    (ROOT/'qa'/'render_manifest.json').write_text(json.dumps({'pdf':pdf.relative_to(ROOT).as_posix(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':len(doc),'sheets':sheets,'pages_changed_since_previous_render':changed},indent=2),encoding='utf-8')
    print(f'Rendered {len(doc)} pages into {len(sheets)} review sheets')
    print('Changed page images:',changed)

if __name__=='__main__':main()
