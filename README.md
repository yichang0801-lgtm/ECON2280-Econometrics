# Estella-Xie

HKU Business School — BEcon & Fin, Year 2

## ECON2280：OLS 回归学习笔记

[直接阅读完整中文 PDF](Econometrics中文版笔记.pdf) · [LaTeX 主文件](main.tex) · [原稿逐页对应表](SOURCE_MAP.csv) · [整合与核对记录](qa/)

本仓库统一维护第 2 至第 4 周的中文笔记，内容包括回归系数解释、拟合优度和 OLS 无偏性。正文、标题、图内标注及附录均使用中文，保留必要的专业缩写与公式变量，并在“整理说明”中给出中文释义。

以根目录 `main.tex` 和 `chapters/` 为唯一编辑入口；编译结果固定为根目录 `Econometrics中文版笔记.pdf`。不再另建名称不同、内容相同的成品文件。原有 GitHub PDF 地址继续可用。

### 内容与版式

- 沿用原 BMO 笔记的 12pt、A4、单面、2cm 页边距及章节、定理版式；保留黄粉高亮和红蓝强调。
- 覆盖全部 23 页原稿，保留例题、练习、证明及重复推导。第 4 周手写页码跳号按练习安排处理。
- 三章分别位于 `chapters/week2.tex`、`week3.tex`、`week4.tex`；附录提供可点击的原稿对应表与 30 条勘误或必要条件补充。
- 8 张图由 Python/Matplotlib 绘制，同时提供矢量 PDF 与 PNG 预览；示意数据及拟合统计量的计算方式已说明。
- 当前 Windows 验收版本为 35 页，含 65 个书签、173 个内部链接和 137 处独立陈列公式。

### 构建

安装 Python 3.11+、XeLaTeX（MiKTeX 或 TeX Live）及所需 Python 库：

```powershell
python -m pip install -r requirements.txt
python scripts/build.py --skip-figures
```

Windows 也可双击 `build.cmd`。省略 `--skip-figures` 会先重绘全部图形；本机重绘使用宋体。仓库内已有完整矢量图，无需重绘也可编译。Windows 使用原字体，其他环境自动使用 Fandol 中文字体；字体差异可能改变分页。

编译脚本依次生成附录、核对数值、多轮运行 XeLaTeX 直至目录与交叉引用稳定，再检查正文、来源锚点、书签、内部链接及译文公式。无需 latexmk 或 Perl。`ctex`、`amsmath`、`amsthm`、`geometry`、`hyperref`、`bookmark`、`booktabs`、`longtable`、`enumitem` 等 LaTeX 包须可用。

### 核对与页面复核

```powershell
python scripts/verify_math.py
python scripts/verify_translation.py
python scripts/verify_delivery.py
python scripts/render_review.py
```

最后一条命令生成 `qa/rendered/` 中的逐页图与检查图。内容改动后须检查新 PDF；`qa/visual_review.json` 的视觉验收只适用于其中记录的准确 PDF 校验值。数学核对包含 17 项独立检查，翻译核对比较全部陈列公式以及标签、例题环境、来源锚点和勘误链接。

### 项目结构

| 路径 | 用途 |
| --- | --- |
| `main.tex` | 中文主文件与统一导言区 |
| `chapters/` | 三章正文、原稿对应表和勘误附录 |
| `figures/` | 8 组矢量图、预览及数值记录 |
| `scripts/` | 构建、绘图、渲染及核对脚本 |
| `sources/manifest.json` | 原稿文件名、大小与校验值，不含本机绝对路径 |
| `template/README.md` | 原模板来源与字体约定 |
| `translation/` | 逐段译文与翻译前源码快照，用于对照追溯 |
| `qa/` | 内容覆盖、数学、译文、交付、视觉及整合记录 |

正常修改直接编辑主文件与分章源码；`translation/` 的历史应用脚本不属于日常构建入口。编译缓存、页面渲染图不纳入 Git。

### 与原版本的关系

本次整合以 GitHub 提交 `1faa5eb45181f80d777b1273cdd16b40f35a2f26` 为起点。仓库原有的主文件、PDF 和全部图形，与本地已验收中文版逐字节一致；本次补齐了当时未上传的分章源码、构建脚本、翻译记录和核对资料。保留原仓库简介及 PDF 文件名，统一说明和构建入口，没有删除学习内容。

本地原中英混排项目、中文版项目及原始扫描稿继续保留。原始扫描稿与完整 BMO 旧笔记不随本次整合上传公开仓库，也不参与编译；详见 [原稿来源说明](sources/README.md)。只有本地存在的原件才会被报告为已完成哈希核验。
