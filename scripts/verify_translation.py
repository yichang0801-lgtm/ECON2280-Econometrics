"""Verify Chinese-edition structure, display mathematics and remaining Latin vocabulary."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import fitz

ROOT=Path(__file__).resolve().parents[1]
PATTERN=re.compile(r'\\\[(.*?)\\\]|\\begin\{(equation\*?|align\*?)\}(.*?)\\end\{\2\}',re.S)

def blocks(text):
    return [m.group(1) if m.group(1) is not None else m.group(3) for m in PATTERN.finditer(text)]

def normalise(text):
    text=re.sub(r'\\text\{[^}]*\}',r'\\TXT',text)
    text=re.sub(r'\\rm\s+(?:Anson|scenario|old|new)',r'\\TXT',text)
    return re.sub(r'\s+','',text)

def main():
    result={}
    for name in ['week2','week3','week4']:
        original=(ROOT/'translation'/'original_tex'/'chapters'/f'{name}.tex').read_text(encoding='utf-8')
        translated=(ROOT/'chapters'/f'{name}.tex').read_text(encoding='utf-8')
        structural={}
        for command in ['label','begin','end','sourcepage','corr','includegraphics']:
            before=re.findall(r'\\'+command+r'\{([^}]+)\}',original)
            after=re.findall(r'\\'+command+r'\{([^}]+)\}',translated)
            assert before==after,(name,command)
            structural[command]=len(before)
        before,after=blocks(original),blocks(translated)
        assert len(before)==len(after)
        reviewed=[]
        for i,(a,b) in enumerate(zip(before,after),1):
            if normalise(a)==normalise(b):continue
            if name=='week2' and i==13:
                # The dollar sign moved into the Chinese word for dollars.
                assert normalise(a).replace(r'\$','')==normalise(b)
                reviewed.append({'block':i,'reason':'货币符号换为中文“美元”；数值及算式不变'})
            elif name=='week2' and i==14:
                assert a.strip()==r'\hp{New scenario wage = old actual wage + modelled change},'
                assert b.strip()==r'\hp{情景工资 = 原实际工资 + 模型给出的变化量},'
                reviewed.append({'block':i,'reason':'高亮框中的纯文字等式完整翻译'})
            else:raise AssertionError((name,i,a,b))
        result[name]={'structure_preserved':structural,'display_math_blocks':len(before),'reviewed_text_only_changes':reviewed}
    pdf=ROOT/'Econometrics中文版笔记.pdf'
    doc=fitz.open(pdf)
    text='\n'.join(p.get_text() for p in doc)
    words=Counter(re.findall(r'[A-Za-z]{3,}',text))
    allowed=set('OLS PDF TSS RSS ACT Sxx FWL SLR Covn ESS MLR wage ZCM Varn colGPA educ hsGPA shareA rji Srjrj income voteA kxk kxki ryi RTO BMO salary roe Corrn xiyi iii sources Python exper tenure rxy BiAi rxi rxiryi xji xki jxji RSSj rjixji rjiyi rjiui jxj SHA manifest json Jintian JTST Matplotlib PRF sxsy colGPAA colGPAB iyi bjxji rxysy rxysx Var Cov log min'.split())
    assert not (set(words)-allowed),sorted(set(words)-allowed)
    forbidden=['Chapter','Contents','Definition','Theorem','Example','Exercise','Figure','Interpretation','Unbiasedness','Goodness','Anson','Betty']
    for word in forbidden:assert not re.search(r'\b'+word+r'\b',text),word
    assert len(doc.get_toc())==65
    report={'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'status':'passed','chapters':result,
       'total_display_math_blocks':sum(v['display_math_blocks'] for v in result.values()),
       'remaining_latin_vocabulary':dict(words),'latin_policy':'仅保留专业缩写、数学记号、原变量名、作者署名、软件名称与文件路径；不存在英文叙述或英文标题'}
    (ROOT/'qa'/'translation_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Translation checks passed:',report['total_display_math_blocks'],'display-math blocks; all source anchors and learning environments preserved')

if __name__=='__main__':main()
