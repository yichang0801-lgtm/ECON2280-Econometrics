"""Apply the reviewed Chinese translations to the preserved source snapshot."""
from pathlib import Path
import json
import hashlib
import shutil

ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/'translation'/'original_tex'
if not SNAP.exists():
    SNAP.mkdir()
    for name in ['main.tex','chapters/week2.tex','chapters/week3.tex','chapters/week4.tex']:
        target=SNAP/name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(ROOT/name,target)

env_titles={
 'Education and wages':'教育与工资', 'Hourly wage: 注意单位':'小时工资：注意单位',
 'Election expenditure':'竞选支出', 'College GPA':'大学平均绩点',
 'GPA: controls change the interpretation':'平均绩点：控制变量改变系数解释',
}
counts={}
for name in ['week2','week3','week4']:
    lines=(SNAP/'chapters'/f'{name}.tex').read_text(encoding='utf-8').splitlines()
    translations={}
    for item in (ROOT/'translation'/f'{name}.txt').read_text(encoding='utf-8').splitlines():
        index,replacement=item.split('|',1)
        assert int(index) not in translations
        translations[int(index)]=replacement
    for index,replacement in translations.items():lines[index-1]=replacement
    text='\n'.join(lines)+'\n'
    for en,zh in env_titles.items():text=text.replace('['+en+']','['+zh+']')
    text=text.replace('对应 $y$ 大约增加 $100\\beta_1$ 个百分点的百分比变化，即变化率约为 $100\\beta_1\\%$','对应 $y$ 的变化率约为 $100\\beta_1\\%$')
    text=text.replace('原稿的 salary--roe 例式','原稿的薪酬与净资产收益率例式')
    text=text.replace('{last page}','{末页}')
    (ROOT/'chapters'/f'{name}.tex').write_text(text,encoding='utf-8')
    counts[name]=len(translations)

text=(SNAP/'main.tex').read_text(encoding='utf-8')
text=text.replace(r'\title{\textbf{OLS Regression Lecture Notes}\\[0.5em]\large Interpretation, Goodness of Fit, and Unbiasedness}',r'\title{\textbf{OLS 回归学习笔记}\\[0.5em]\large 系数解释、拟合优度与无偏性\\[0.5em]\normalsize 完整中文译本}')
text=text.replace(r'\date{Weeks 2--4\\20 October 2026}',r'\date{第 2 至第 4 周\\2026 年 10 月 20 日}')
text=text.replace(r'\usepackage[english]{babel}','')
text=text.replace('UTF8,scheme=plain,fontset=windows','UTF8,scheme=plain,fontset=windows,heading=true')
text=text.replace('pdftitle={OLS Regression Notes - Weeks 2-4}','pdftitle={OLS 回归学习笔记：第 2 至第 4 周（中文版）}')
for en,zh in [('Definition','定义'),('Theorem','定理'),('Lemma','引理'),('Example','例题'),('Exercise','练习')]:
    text=text.replace('{'+en+'}','{'+zh+'}')
text=text.replace(r'\begin{document}',r'''\ctexset{chapter={name={第,章},number=\chinese{chapter}}}
\renewcommand{\contentsname}{目录}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\renewcommand{\proofname}{证明}
\begin{document}''')
text=text.replace(r'\appendix',r'\appendix'+'\n'+r'\ctexset{chapter={name={附录,},number=\Alph{chapter}}}')
text=text.replace('本笔记依据 Week 2--4 的三份手写扫描稿整理，共 23 页。保留英文正文、中文批注、原有例题与证明的顺序；黄色和粉色重点、红蓝说明按原稿用途保留。版式直接沿用既有 BMO CAMP 笔记的 \\texttt{report} 模板。','本笔记依据第 2 至第 4 周的三份手写扫描稿整理，共 23 页。本版将原整理稿的正文、标题、图注、图内标注及附录全部译为中文，保留原有批注、例题、练习、证明及重复推导的顺序；必要的专业缩写、公式变量和人名保留原记号。黄色和粉色重点、红蓝说明沿用原稿用途。版式仍直接采用既有 BMO 笔记模板。')
start=text.index(r'\paragraph{Notation.}')
end=text.index('\n\n',start)
text=text[:start]+r'''\paragraph{记号约定。}$\beta_j$ 表示固定的总体参数；$\hat\beta_j$ 表示 OLS 估计量，或在样本已固定时表示它的实现值。$u_i$ 是总体误差，$\hat u_i=y_i-\hat y_i$ 是拟合残差。需要区分时，样本协方差、方差和相关系数明确加下标 $n$。$k$ 为\emph{不含截距}的回归变量个数，$n$ 为样本量。

\paragraph{公式中的英文变量。}为便于与原题核对，公式保留原变量名：$\wage$ 为工资，$\educ$ 为教育年限，$\mathrm{salary}$ 为薪酬，$\mathrm{roe}$ 为净资产收益率，$\colGPA$ 为大学平均绩点，$\hsGPA$ 为高中平均绩点，$\ACT$ 为 ACT 考试分数，$\mathrm{income}$ 为收入，$\mathrm{exper}$ 为工作经验，$\mathrm{tenure}$ 为任职年限；$\mathrm{voteA}$ 与 $\mathrm{shareA}$ 分别为候选人 A 的得票百分比和竞选支出百分比。OLS 指普通最小二乘法，FWL 指弗里施—沃—洛维尔定理，SLR 与 MLR 分别是简单线性回归和多元线性回归假设的编号前缀。''' + text[end:]
(ROOT/'main.tex').write_text(text,encoding='utf-8')
(ROOT/'qa'/'translation_record.json').write_text(json.dumps({'language':'zh-CN','translated_lines':counts,'source_snapshot':'translation/original_tex','scope':'正文、标题、图注、图内标注、附录；保留专业缩写与公式变量','original_project_unchanged':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('Applied chapter translations:',counts)
