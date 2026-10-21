"""Editorial provenance and correction records; no source content is deleted."""
from pathlib import Path
import csv
import json

ROOT=Path(__file__).resolve().parents[1]
pages=[(2, 1, '2/1', '简单模型；其他条件不变；误差归一化；零条件均值；工资例题'), (2, 2, '2/2', '总体回归函数推导；OLS 系数；相关与因果；截距；薪酬示意图'), (2, 3, '2/3', '工资单位练习；安森的假设情景；得票与竞选支出练习'), (2, 4, '2/4', '多元偏效应；相关的控制变量；平均绩点解释；安森与贝蒂'), (2, 5, '2/5', '控制变量；能力；保持不变；单侧及一般 FWL 定理'), (2, 6, '2/6', '短回归与长回归；系数相同的条件；舍入后的绩点方程'), (2, 7, '2/7', '因变量与自变量单位变换；截距解释；样本协方差推导'), (2, 8, '末页，按 PDF 定位', '水平值与对数的四类模型；百分比解释'), (3, 1, '3/1', '误差与残差；简单 OLS 的三个样本性质；总体矩条件'), (3, 2, '3/2', '三类平方和；交叉项证明；完全拟合；判定系数的相关解释'), (3, 3, '3/3', '判定系数比较图；再次保留多元 OLS 性质及证明'), (3, 4, '3/4', '增加回归变量；调整判定系数；绩点数值核算；三点提醒'), (3, 5, '3/5', '过原点估计；去均值；均值点示意图；页底重复的工资例式'), (3, 6, '补充推导页', '再次保留有无截距的公式；去均值；仅含常数项的回归；FWL'), (3, 7, '3/6', '再次保留过原点回归一阶条件；样本性质；协方差限制；负判定系数'), (4, 1, '4/1', '学习目标；估计回顾；参数与估计量；无偏性；简单回归假设概览'), (4, 2, '4/2', '简单回归假设详解；总体误差示意图；斜率无偏性的证明'), (4, 3, '4/3', '考试提示中的截距证明；违背假设的后果及结论边界'), (4, 4, '4/5', '多元回归前三项假设；常数自变量示意图；全部完全共线性例子'), (4, 5, '4/6', '多元回归第四项假设；无偏性定理；辅助残差性质；FWL 期望证明'), (4, 6, '4/7', '控制变量与无偏性回顾；假设对照表；某次对数工资估计'), (4, 7, '4/8', '无关控制变量；遗漏相关变量；短长回归的精确样本恒等式'), (4, 8, '4/9', '迭代期望偏误证明；附加条件；偏误方向与符号表')]

# id, source anchors, title, corrected statement and reason, reference group
corrections=[
 ('notation',[(2,4),(3,1)],'总体、估计量与拟合值记号',r'总体参数写作 $\beta_j$，样本估计写作 $\hat\beta_j$；总体误差 $u_i$ 与残差 $\hat u_i$ 分开。拟合值变化使用 $\Delta\hat y$，不将 $\hat\beta_j$ 直接写成总体参数。','H1'),
 ('mean-normalisation',[(2,1)],'误差均值的归一化',r'令 $\varepsilon=u-\alpha$ 后，$\E[\varepsilon]=0$，而不是 $\varepsilon$ 处处等于零。截距变为 $\beta_0+\alpha$。该归一化本身不保证零条件均值。','H1'),
 ('slope-correlation',[(2,2)],'斜率与相关系数的比例',r'样本简单 OLS 斜率为 $r_{xy}s_y/s_x$，不是 $r_{xy}s_x/s_y$；总体投影系数和样本系数不能混用。','H2'),
 ('causality',[(2,2),(2,4)],'相关与因果的边界',r'保留“相关联”的措辞；控制变量、ZCM 或好的拟合度本身不能替代结构模型与可辩护的因果识别。截距在 $x=0$ 不可行时只是外推。','H1'),
 ('wage-counterfactual',[(2,3)],'工资题中的单位与个体反事实',r'按原稿“千美元”复算：$5.58$、$-5.574$、$7.74$、$2.166$ 均使用同一单位。固定该人残差得到的是模型情景，并非保证的实际工资。未把看似异常的原题单位擅自改成美元。','计算'),
 ('election',[(2,3)],'选举题的比例与金额',r'40\% 应输入 40，预测为 45.37\%；50\% 的预测阈值对应 支出占比 $>49.978448\ldots$。补齐在 B 支出 20 亿美元时 A 的支出阈值，区别预测过半与实际获胜。','计算'),
 ('fwl-residual',[(2,5),(4,5)],'FWL 的单侧与双侧残差化',r'只残差化自变量后回归原始 $y$，系数相同，但残差一般不等于原多元模型残差。对 $y$ 与该自变量同时排除其他回归量，才能同时得到相同系数与残差。','H2'),
 ('ovb-levels',[(2,6),(4,8)],'遗漏变量公式的三个层次',r'保留样本恒等式 $\hat{\tilde\beta}_1=\hat\beta_1+\hat\beta_2\hat\delta_1$。给定整组设计时，偏差为 $\beta_2\hat\delta_1$；无条件有限样本偏差为 $\beta_2\E[\hat\delta_1]$。写成 $\beta_2\delta_1$ 还须有辅助斜率无偏等附加条件；总体投影差另行说明。','H3'),
 ('unit-intercept',[(2,7)],'换单位时的截距与条件均值',r'总体截距的含义是 $\E[y\mid x=0]$，不是一般的 $\E[y]$；$y$ 乘以 $c$ 时截距也乘以 $c$。$x$ 乘以非零 $c$ 时斜率除以 $c$，截距不变。','计算'),
 ('logs',[(2,8)],'有限变化与对数近似',r'将有限变化的近似与精确关系分开。水平值—对数模型为 $\beta_1\ln(x_1/x_0)$；对数—水平值模型的精确百分比为 $100(e^{\beta_1\Delta x}-1)$；对数—对数模型使用比例的幂。对数模型的系数仍保留原稿的局部百分比解释。','计算'),
 ('sample-population',[(3,1)],'样本恒等式不是总体外生性的检验',r'残差和为零、与包含的回归量正交来自样本 OLS 一阶条件。不能从这些条件推出真实误差的 ZCM。总体均值关系用无帽参数，样本均值关系用样本系数。','H2'),
 ('r2-degenerate',[(3,2)],'判定系数 的退化情形',r'补充 TSS 必须大于零。拟合值恒定时，普通 $R^2$ 可以为零，但相关系数因分母为零而未定义；此时不能直接用相关系数平方计算。','H2'),
 ('r2-rss',[(3,3)],'高拟合度与 RSS 的比较',r'高 $R^2$ 表示较小的 RSS/TSS；不能跨不同样本或单位仅凭较高 $R^2$ 就认定绝对 RSS 更小。图中 0.94 和 0.64 均由新绘制的示意点实际计算。','H2'),
 ('r2-monotonic',[(3,4)],'增加回归量时 判定系数 不减',r'原稿的“增加”改为“不下降，可以保持不变”，并注明必须是相同观测、相同因变量的嵌套 OLS 比较。不同缺失值样本不在该结论内。','H2'),
 ('adjusted-meaning',[(3,4)],'调整判定系数 的提高条件',r'“变量有意义才提高”改写为残差均方必须下降；增加 $q$ 个回归量时，对应描述性的 偏 F 统计量 大于 1。这个阈值不是常规显著性检验，也不证明因果。','计算'),
 ('demeaning',[(3,5),(3,6)],'去均值与过原点回归',r'是“去均值后无截距”的斜率等于“原始数据带截距”的斜率；不是任意无截距回归都等于带截距回归。原稿的两次推导均保留。','H2'),
 ('rto-covariance',[(3,7)],'无截距时的正交与不相关',r'$\sum_i x_i\check u_i=0$ 仍成立，但 $\Cov_n(x,\check u)=-\bar x\bar{\check u}$ 一般不为零。原稿将两者等同的说法已改正。','H2'),
 ('rto-cross-term',[(3,7)],'平方和分解的交叉项',r'交叉项应为 $2\sum_i\check u_i(\hat y_i-\bar y)$，其中是拟合值 $\hat y_i$。无截距时它不一定消失，因此不能一般地写 TSS=ESS+RSS。','H2'),
 ('rto-r2',[(3,7)],'有截距与无截距 判定系数 的基准',r'区分以样本均值为基准的 中心化判定系数 与以零为基准的 非中心化判定系数。前者在过原点回归中可以为负；两种统计量不能当作同一尺度直接比较。','M'),
 ('estimator-estimate',[(4,1)],'估计量与某次估计值',r'无偏性不要求某一次估计等于真值，也不声称每一次估计必定不等于真值。它是对重复抽样期望的限制，并需要相关期望存在。','H3'),
 ('conditioning',[(4,2),(4,5)],'无偏性证明的条件期望',r'先给定整组样本设计，再将样本权重与分母作为常量提出条件期望。不能仅使用单个 $x_i$ 的条件，或在无条件期望中把随机分母当常数。注明样本满秩和期望存在。','H3'),
 ('intercept-sign',[(4,3)],'截距证明的正负号',r'从总体模型取平均得到 $\bar y=\beta_0+\beta_1\bar x+\bar u$；因此截距展开式中的 $\bar u$ 应为加号。原稿中间一行的减号与其余推导不一致。','计算'),
 ('violations',[(4,3)],'违背抽样假设的后果',r'保留时间序列相关、非代表性样本和溢出效应的例子；将它们与“必然产生 OLS 偏差”区分。需另查条件均值，不能仅凭违反独立同分布假设 就推出所有系数有偏。','H3'),
 ('zcm-covariance',[(4,3),(4,5)],'ZCM 强于零协方差',r'$\E[u\mid x]=0$ 推出零均值、零协方差；反方向不成立。总体误差不相关不足以保证有限样本无偏；与样本残差正交也不构成外生性的证据。','H1'),
 ('collinearity',[(4,4)],'完全共线性与平方项',r'保留常数、倍数、仿射关系、总支出等例子。对数变量及其平方一般不自动完全共线，但特殊样本仍可能不满秩；“样本满秩所以总体一定如何”的措辞改为直接检查样本设计。','H3'),
 ('unbiased-log',[(4,6)],'9.2\% 与无偏估计程序',r'改正 $\log(\widehat{wage})$ 与 $\widehat{\log(wage)}$ 的混用。0.092 是一个实现值；OLS 系数估计量的无偏不保证指数变换无偏。9.2\% 是近似，精确的固定误差变换约为 9.64\%。','H3'),
 ('irrelevant-exogeneity',[(4,7)],'加入无关变量需要扩充后的外生性',r'不能从 $\E[u\mid x_1,x_2]=0$ 自动推出加入 $x_3$ 后条件均值仍为零。仅在扩充后满秩且继续满足 ZCM 等条件时，原有系数及零系数的 OLS 估计量才保持无偏。','H3'),
 ('irrelevant-variance',[(4,7)],'无关控制变量与精度',r'将“估计方差必然上升”限定为同方差固定设计下，加入无关控制使相关真实条件方差弱增；不保证严格增加，也不保证每次实现的估计标准误增加。','H3'),
 ('omitting-relevant',[(4,7)],'遗漏相关变量的条件',r'小节标题按内容改为 遗漏相关变量；遗漏变量系数非零并不足以保证目标斜率改变，还要看它与保留回归量的关系。误差、短回归残差、长回归残差分开。','H3'),
 ('toward-zero',[(4,8)],'向零偏不能只看上偏或下偏',r'保留正系数下偏、负系数上偏的方向解释，但增加“不越过零”的限制。发生符号反转时不能仅按方向就称为通常意义的向零偏。','计算'),
]

def main():
    (ROOT/'qa'/'editorial_records.json').write_text(json.dumps({'pages':[{'week':w,'pdf_page':p,'handwritten':h,'coverage':t,'anchor':f'src:w{w}p{p}','reviewed':True} for w,p,h,t in pages], 'corrections':[{'id':i,'sources':s,'title':t,'correction_tex':b,'reference':r} for i,s,t,b,r in corrections], 'substantive_unresolved_handwriting':[], 'page_number_note':'第 4 周跳号按用户说明属于练习安排；第 2 周末页按 PDF 页码定位，不猜写手写末位数字。'},ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'SOURCE_MAP.csv').open('w',encoding='utf-8-sig',newline='') as f:
        wr=csv.writer(f);wr.writerow(['week','pdf_page','handwritten_page','content_covered','latex_anchor'])
        for w,p,h,t in pages:wr.writerow([w,p,h,t,f'src:w{w}p{p}'])
    tex=[r'\chapter{原稿对应表}',r'\label{app:sources}',
         '每行对应一页原始 PDF；点击正文页码可跳到该页内容开始的位置。跨页内容仍按原稿顺序衔接。所有 23 页均逐页查看，原稿中的重复讲解、例式和页底可见片段均保留。',
         '第 4 周的手写页码跳号按用户说明属于练习安排，不标记为漏扫；不补写未提供的练习。第 2 周末页的手写页码以 PDF 第 8 页定位，避免猜写最后一位。',
         r'\small\renewcommand{\arraystretch}{1.25}',
         r'\begin{longtable}{P{1.05cm}P{.8cm}P{2.25cm}P{9.7cm}P{.9cm}}',
         r'\toprule 周次 & PDF & 手写页码 & 已整理内容 & 页码\\\midrule\endfirsthead',
         r'\toprule 周次 & PDF & 手写页码 & 已整理内容 & 页码\\\midrule\endhead',
         r'\bottomrule\endfoot']
    for w,p,h,t in pages:
        tex.append(f'{w} & {p} & {h} & {t} & '+rf'\hyperref[src:w{w}p{p}]{{\pageref*{{src:w{w}p{p}}}}}\\')
    tex.extend([r'\end{longtable}\normalsize',r'\section*{复现与原件}',
                '原始 PDF 和 BMO 模板副本保持原样；文件路径、字节数及 SHA256 校验值见项目中的 sources/manifest.json。矢量图和对应预览由同一 Python 脚本生成，数值检查记录另保存在 qa 目录。'])
    (ROOT/'chapters'/'source_map.tex').write_text('\n'.join(tex)+'\n',encoding='utf-8')
    tex=[r'\chapter{勘误与补充说明}',r'\label{app:errata}',
         '正文直接采用正确写法；本附录记录实质修正及必要条件补充。原稿本来正确的结论不因列入此处而被视为错误；部分条目只是限制适用范围或明确记号。点原稿定位可返回正文；未删除原稿学习内容。',
         r'\section*{核对依据}',
         r'\begin{description}',
         r'\item[H1.] 汉森，\emph{计量经济学}，2010 年 1 月 10 日稿，第 2 章：条件均值、投影与解释。 \href{https://users.ssc.wisc.edu/~xshi28/Econometrics_Hansen.pdf}{大学网站公开的教材手稿}.',
         r'\item[H2.] 同一手稿，第 3.3 至 3.7 节及第 3.10 节：OLS 代数、残差回归与拟合优度。',
         r'\item[H3.] 同一手稿，第 4.3、4.4、4.11、4.12 节：条件无偏性、方差、共线性与遗漏变量。本笔记还明确推导了额外的有限样本限定条件。',
         r'\item[M.] 梅西大学， \href{https://r-resources.massey.ac.nz/161251/lectures/RegressionOrigin.html}{\emph{过原点回归}}: 中心化与非中心化拟合统计量的比较。',
         r'\item[计算.] 对原稿算式直接进行代数推导或数值运算；项目中包含可复现的数值核对。',
         r'\end{description}',
         '外部材料仅用于核对数学与适用条件；本次排版模板仍是用户指定的旧 BMO 笔记。']
    for n,(key,srcs,title,body,ref) in enumerate(corrections,1):
        links='；'.join(rf'\hyperref[src:w{w}p{p}]{{第 {w} 周，PDF 第 {p} 页}}' for w,p in srcs)
        tex.extend([r'\par\medskip\noindent\begin{minipage}{\linewidth}',rf'\phantomsection\label{{err:{key}}}',
                    rf'\textbf{{C{n:02d}. {title}}}\quad\textbf{{原稿定位：}}{links}。\quad\textbf{{核对：}}{ref}。\par',
                    body,r'\end{minipage}\par'])
    (ROOT/'chapters'/'errata.tex').write_text('\n\n'.join(tex)+'\n',encoding='utf-8')
    print(f'Generated {len(pages)} source mappings and {len(corrections)} correction records')

if __name__=='__main__':main()
