"""Check preserved sources, coverage anchors, PDF text, bookmarks and links."""
from pathlib import Path
import hashlib
import json
import re
import fitz

ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'sources'/'manifest.json').read_text(encoding='utf-8'))
    source_checks=[]
    for item in manifest['sources']:
        path=ROOT/item['copy']
        present=path.exists()
        if present:assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        source_checks.append({'week':item['week'],'present':present,'sha256_verified':present})
    template_path=ROOT/manifest['template']['copy']
    if template_path.exists():
        assert hashlib.sha256(template_path.read_bytes()).hexdigest()==manifest['template']['sha256']
    # Scans and the full unrelated BMO notes are retained locally, not required to build.
    expected={(2,p) for p in range(1,9)}|{(3,p) for p in range(1,8)}|{(4,p) for p in range(1,9)}
    source='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'chapters').glob('week*.tex'))
    actual=[tuple(map(int,m)) for m in re.findall(r'\\sourcepage\{(\d+)\}\{(\d+)\}',source)]
    assert set(actual)==expected and len(actual)==23
    records=json.loads((ROOT/'qa'/'editorial_records.json').read_text(encoding='utf-8'))
    assert not records['substantive_unresolved_handwriting']
    alltex=source+'\n'+(ROOT/'main.tex').read_text(encoding='utf-8')
    used=set(re.findall(r'\\corr\{([^}]+)\}',alltex))
    defined={item['id'] for item in records['corrections']}
    assert used<=defined,(used-defined)
    pdf=ROOT/'Econometrics中文版笔记.pdf';doc=fitz.open(pdf)
    text='\n'.join(page.get_text() for page in doc)
    assert '??' not in text and '\ufffd' not in text
    for token in ['回归的解释','拟合优度','无偏性','原稿对应表','勘误与补充说明','零条件']:
        assert token in text,token
    links=[link for p in doc for link in p.get_links()]
    internal=[l for l in links if l['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and 'page' in l]
    unresolved=[l for l in links if l['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and 'page' not in l]
    assert not unresolved,unresolved
    assert internal and all(0<=l.get('page',-1)<len(doc) for l in internal)
    toc=doc.get_toc();assert len(toc)>15
    possible_overflow=[]
    for i,p in enumerate(doc):
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if x0<12 or x1>p.rect.width-12 or y0<8 or y1>p.rect.height-8:
                        possible_overflow.append({'page':i+1,'text':span['text'],'bbox':span['bbox']})
    pdf_hash=hashlib.sha256(pdf.read_bytes()).hexdigest()
    review_path=ROOT/'qa'/'visual_review.json'
    review=json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
    visual_passed=review.get('pdf_sha256')==pdf_hash and review.get('status')=='passed'
    report={'pdf':pdf.relative_to(ROOT).as_posix(),'pdf_sha256':pdf_hash,'pages':len(doc),'searchable_characters':len(text),'source_pages_mapped':len(actual),
       'correction_records':len(defined),'bookmarks':len(toc),'internal_links':len(internal),'external_links':len(links)-len(internal),
       'source_hashes_verified':all(i['sha256_verified'] for i in source_checks),'source_checks':source_checks,
       'template_hash_verified':template_path.exists(),'optional_originals_required_for_build':False,'missing_reference_markers':False,
       'substantive_unresolved_handwriting':[],'possible_page_edge_overflow':possible_overflow,
       'visual_review':'passed for this exact PDF' if visual_passed else 'pending; render and inspect final pages before delivery'}
    (ROOT/'qa'/'delivery_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'qa'/'pdf_text.txt').write_text(text,encoding='utf-8')
    print(f'Delivery checks passed: {len(doc)} pages, {len(internal)} internal links, {len(toc)} bookmarks')
    if possible_overflow:print('Potential page-edge overflow spans:',len(possible_overflow))

if __name__=='__main__':main()
