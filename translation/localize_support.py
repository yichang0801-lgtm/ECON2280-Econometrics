"""Localize appendix generation, figures and delivery checks for the Chinese edition."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

path=ROOT/'scripts'/'generate_appendices.py'
text=path.read_text(encoding='utf-8')
start=text.index('pages=[');end=text.index('\n]\n',start)+3
pages=[
 (2,1,'2/1','简单模型；其他条件不变；误差归一化；零条件均值；工资例题'),
 (2,2,'2/2','总体回归函数推导；OLS 系数；相关与因果；截距；薪酬示意图'),
 (2,3,'2/3','工资单位练习；安森的假设情景；得票与竞选支出练习'),
 (2,4,'2/4','多元偏效应；相关的控制变量；平均绩点解释；安森与贝蒂'),
 (2,5,'2/5','控制变量；能力；保持不变；单侧及一般 FWL 定理'),
 (2,6,'2/6','短回归与长回归；系数相同的条件；舍入后的绩点方程'),
 (2,7,'2/7','因变量与自变量单位变换；截距解释；样本协方差推导'),
 (2,8,'末页，按 PDF 定位','水平值与对数的四类模型；百分比解释'),
 (3,1,'3/1','误差与残差；简单 OLS 的三个样本性质；总体矩条件'),
 (3,2,'3/2','三类平方和；交叉项证明；完全拟合；判定系数的相关解释'),
 (3,3,'3/3','判定系数比较图；再次保留多元 OLS 性质及证明'),
 (3,4,'3/4','增加回归变量；调整判定系数；绩点数值核算；三点提醒'),
 (3,5,'3/5','过原点估计；去均值；均值点示意图；页底重复的工资例式'),
 (3,6,'补充推导页','再次保留有无截距的公式；去均值；仅含常数项的回归；FWL'),
 (3,7,'3/6','再次保留过原点回归一阶条件；样本性质；协方差限制；负判定系数'),
 (4,1,'4/1','学习目标；估计回顾；参数与估计量；无偏性；简单回归假设概览'),
 (4,2,'4/2','简单回归假设详解；总体误差示意图；斜率无偏性的证明'),
 (4,3,'4/3','考试提示中的截距证明；违背假设的后果及结论边界'),
 (4,4,'4/5','多元回归前三项假设；常数自变量示意图；全部完全共线性例子'),
 (4,5,'4/6','多元回归第四项假设；无偏性定理；辅助残差性质；FWL 期望证明'),
 (4,6,'4/7','控制变量与无偏性回顾；假设对照表；某次对数工资估计'),
 (4,7,'4/8','无关控制变量；遗漏相关变量；短长回归的精确样本恒等式'),
 (4,8,'4/9','迭代期望偏误证明；附加条件；偏误方向与符号表'),
]
text=text[:start]+'pages='+repr(pages)+'\n'+text[end:]
replacements={
 '保留 associated with 的措辞':'保留“相关联”的措辞',
 'shareA $>49.978448':'支出占比 $>49.978448',
 'level--log 为':'水平值—对数模型为',
 'log--level 的精确百分比':'对数—水平值模型的精确百分比',
 'log--log 使用比例的幂':'对数—对数模型使用比例的幂',
 'R-squared':'判定系数', 'Adjusted 判定系数':'调整判定系数',
 'partial-F':'偏 F 统计量',
 'uncentred 判定系数':'非中心化判定系数','centred 判定系数':'中心化判定系数',
 '和 spillover 的例子':'和溢出效应的例子',
 '违反 i.i.d.':'违反独立同分布假设',
 '9.2 percent 与无偏估计程序':'9.2\\% 与无偏估计程序',
 'estimated variance 必然上升':'估计方差必然上升',
 'Omitting a relevant variable':'遗漏相关变量',
 'Week 4 jump is an exercise arrangement per user; Week 2 final handwritten numeral is not used as a guessed locator.':'第 4 周跳号按用户说明属于练习安排；第 2 周末页按 PDF 页码定位，不猜写手写末位数字。',
 'Week4 的手写页码跳号按用户说明属于 exercise 安排':'第 4 周的手写页码跳号按用户说明属于练习安排',
 'Week2 末页的手写页码':'第 2 周末页的手写页码',
 r'\toprule Week & PDF':'\\toprule 周次 & PDF',
 'Hansen, \\emph{Econometrics}, 10 January 2010, Chapter 2: conditional means, projection and interpretation.':'汉森，\\emph{计量经济学}，2010 年 1 月 10 日稿，第 2 章：条件均值、投影与解释。',
 'University-hosted manuscript':'大学网站公开的教材手稿',
 'The same manuscript, Sections 3.3--3.7 and 3.10: OLS algebra, residual regression and measures of fit.':'同一手稿，第 3.3 至 3.7 节及第 3.10 节：OLS 代数、残差回归与拟合优度。',
 'The same manuscript, Sections 4.3, 4.4, 4.11 and 4.12: conditional unbiasedness, variance, collinearity and omitted variables. Additional finite-sample qualifications are derived explicitly in these notes.':'同一手稿，第 4.3、4.4、4.11、4.12 节：条件无偏性、方差、共线性与遗漏变量。本笔记还明确推导了额外的有限样本限定条件。',
 'Massey University,':'梅西大学，',
 r'\emph{Regression through the origin}':'\\emph{过原点回归}',
 'centred versus uncentred fit statistics.':'中心化与非中心化拟合统计量的比较。',
 'Direct algebra or arithmetic from the supplied note; reproducible numerical checks are included in the project.':'对原稿算式直接进行代数推导或数值运算；项目中包含可复现的数值核对。',
 r'\item[calc.]':r'\item[计算.]',
 "'calc')":"'计算')",
 "{Week {w}, PDF {p}}":"{第 {w} 周，PDF 第 {p} 页}",
}
# Translate the hyperlink label in an f-string without changing its brace structure.
text=text.replace('{{Week {w}, PDF {p}}}','{{第 {w} 周，PDF 第 {p} 页}}')
for en,zh in replacements.items():text=text.replace(en,zh)
path.write_text(text,encoding='utf-8')

path=ROOT/'scripts'/'draw_figures.py'
text=path.read_text(encoding='utf-8')
text=text.replace("'font.serif': ['DejaVu Serif']","'font.serif': ['SimSun', 'DejaVu Serif']")
text=text.replace("'mathtext.fontset': 'cm'","'axes.unicode_minus': False, 'mathtext.fontset': 'cm'")
for en,zh in {
 'Fitted line (one sample)':'拟合线（某一样本）',
 'Population line (schematic)':'总体线（示意）',
 'Return on equity, roe (percentage points)':'净资产收益率（百分点）',
 "ax.set_ylabel('Salary')":"ax.set_ylabel('薪酬')",
 'With intercept':'含截距', 'Demeaned: same slope':'去均值：斜率不变',
 'Forced through origin':'强制过原点拟合',
 r'Mean-only baseline $\bar y$':r'仅含均值的基准 $\bar y$',
 'Centered $R^2=':'中心化 $R^2=',
 r'$x_i=c$ for every $i$':r'对所有 $i$，$x_i=c$',
 r'$\beta_0+c\beta_1$: only the sum is identified':r'$\beta_0+c\beta_1$：只能识别这一总和',
}.items():text=text.replace(en,zh)
path.write_text(text,encoding='utf-8')

for name in ['build.py','verify_delivery.py','render_review.py']:
    path=ROOT/'scripts'/name
    text=path.read_text(encoding='utf-8').replace('Econometrics_OLS_Notes.pdf','Econometrics_OLS_Notes_ZH.pdf')
    text=text.replace("['Interpretation','Goodness','Unbiasedness','原稿对应表','勘误与补充说明','零条件']","['回归的解释','拟合优度','无偏性','原稿对应表','勘误与补充说明','零条件']")
    path.write_text(text,encoding='utf-8')
path=ROOT/'build.cmd'
path.write_bytes(path.read_bytes().replace(b'Econometrics_OLS_Notes.pdf',b'Econometrics_OLS_Notes_ZH.pdf'))
print('Localized appendix generator, eight figures and build pipeline')
