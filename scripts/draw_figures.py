"""Recreate the instructional diagrams; all plotted observations are schematic."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
logging.getLogger('fontTools.ttLib.tables._h_e_a_d').setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['SimSun', 'DejaVu Serif'],
    'axes.unicode_minus': False, 'mathtext.fontset': 'cm', 'font.size': 11, 'axes.labelsize': 12,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': .8, 'lines.linewidth': 1.5, 'savefig.bbox': 'tight',
    'pdf.fonttype': 42, 'ps.fonttype': 42})
BLUE, RED, GREY = '#213676', '#99272b', '#6a6a6a'
stats = {}

def save(fig, name):
    fig.savefig(OUT / f'{name}.pdf', facecolor='white')
    fig.savefig(OUT / f'{name}.png', dpi=180, facecolor='white')
    plt.close(fig)

def quiet(ax):
    ax.tick_params(direction='out', length=3, width=.7)
    ax.set_xlabel('$x$'); ax.set_ylabel('$y$', rotation=0, labelpad=12)

fig, ax = plt.subplots(figsize=(7.2, 3.3), layout='constrained')
x = np.linspace(0, 5.5, 200); b0, b1 = 1, .65
ax.plot(x, b0+b1*x, color=BLUE)
for j, xi in enumerate([1.1, 2.7, 4.3], 1):
    mu=b0+b1*xi; ys=np.linspace(mu-1.05,mu+1.05,100)
    density=.55*np.exp(-.5*((ys-mu)/.4)**2)
    ax.plot(xi+density,ys,color=GREY,lw=1)
    ax.vlines(xi,0,mu,color=GREY,lw=.7,linestyle=':')
    ax.scatter([xi],[mu],s=24,c=BLUE,zorder=3)
    ax.text(xi,-.3,f'$x_{j}$',ha='center')
ax.text(.5,4.7,r'$E[y\mid x]=\beta_0+\beta_1x$',color=BLUE)
ax.text(-.13, b0, r'$\beta_0$',ha='right',va='center')
ax.set_xlim(-.1,5.6);ax.set_ylim(-.45,5.2);ax.set_xticks([]);ax.set_yticks([])
quiet(ax);save(fig,'conditional_means')

fig, ax=plt.subplots(figsize=(6.4,3),layout='constrained')
x=np.linspace(0,30,100)
ax.plot(x,963.191+18.501*x,color=BLUE,label='拟合线（某一样本）')
ax.plot(x,1050+13*x,color=GREY,ls='--',label='总体线（示意）')
ax.set_xlabel('净资产收益率（百分点）');ax.set_ylabel('薪酬')
ax.text(10,1020,r'$\widehat{salary}=963.191+18.501\,roe$',color=BLUE)
ax.legend(frameon=False,loc='upper left',fontsize=9);save(fig,'fitted_population')

x=np.linspace(.4,5.2,25);xc=x-x.mean();signal=.9*xc
raw=np.sin(np.arange(len(x))*2.41)+.4*np.cos(np.arange(len(x))*.77)
design=np.column_stack([np.ones(len(x)),x]);e=raw-design@np.linalg.lstsq(design,raw,rcond=None)[0]
fig, axs=plt.subplots(1,2,figsize=(8.3,3.2),layout='constrained')
for ax,target in zip(axs,[.94,.64]):
    err=e*np.sqrt(np.dot(signal,signal)*(1-target)/(target*np.dot(e,e)))
    y=3+signal+err;fit=design@np.linalg.lstsq(design,y,rcond=None)[0]
    actual=1-np.sum((y-fit)**2)/np.sum((y-y.mean())**2)
    assert abs(actual-target)<1e-12
    stats[f'r2_{target:.2f}']=actual
    ax.scatter(x,y,s=16,color=BLUE);ax.plot(x,fit,color=GREY)
    ax.set_title(f'$R^2={actual:.2f}$',fontsize=12);quiet(ax)
    ax.set_xlim(0,5.6);ax.set_ylim(-.2,6.3)
save(fig,'r_squared_comparison')

fig,axs=plt.subplots(1,2,figsize=(8.3,3),layout='constrained')
x=np.array([1.,2.,3.,4.,5.]);y=np.array([2.5,3.1,4.4,4.6,6.4])
b=np.linalg.lstsq(np.column_stack([np.ones(len(x)),x]),y,rcond=None)[0]
for ax,xx,yy,intercept in [(axs[0],x,y,b[0]),(axs[1],x-x.mean(),y-y.mean(),0)]:
    ax.scatter(xx,yy,color=BLUE,s=22);grid=np.linspace(xx.min()-.4,xx.max()+.4,50)
    ax.plot(grid,intercept+b[1]*grid,color=GREY);quiet(ax)
axs[0].scatter([x.mean()],[y.mean()],color=RED,s=35,zorder=3)
axs[0].annotate(r'$(\bar x,\bar y)$',(x.mean(),y.mean()),xytext=(12,-25),textcoords='offset points',color=RED)
axs[0].set_title('含截距',fontsize=11)
axs[1].axhline(0,color=GREY,lw=.5);axs[1].axvline(0,color=GREY,lw=.5)
axs[1].scatter([0],[0],color=RED,s=35,zorder=3);axs[1].set_title('去均值：斜率不变',fontsize=11)
axs[1].set_xlabel(r'$x-\bar x$');axs[1].set_ylabel(r'$y-\bar y$',rotation=0,labelpad=16)
save(fig,'demeaning')

x=np.array([1.,2.,3.,4.,5.]);y=np.array([9.,10.,10.,11.,10.])
bzero=np.dot(x,y)/np.dot(x,x);res=y-bzero*x
r2=1-np.dot(res,res)/np.sum((y-y.mean())**2)
assert r2<0
stats['through_origin']={'slope':float(bzero),'centered_r2':float(r2),'rss':float(np.dot(res,res)),'tss':float(np.sum((y-y.mean())**2))}
fig,ax=plt.subplots(figsize=(6.2,3.2),layout='constrained')
grid=np.linspace(0,5.5,100)
ax.scatter(x,y,s=25,color=BLUE);ax.plot(grid,bzero*grid,color=RED,label='强制过原点拟合')
ax.axhline(y.mean(),color=GREY,ls='--',label=r'仅含均值的基准 $\bar y$')
ax.set_xlim(0,5.5);ax.set_ylim(0,13);quiet(ax)
ax.legend(frameon=False,fontsize=9);ax.text(.35,6.6,f'中心化 $R^2={r2:.2f}$',color=RED)
save(fig,'through_origin_negative_r2')

fig,ax=plt.subplots(figsize=(5.8,2.9),layout='constrained')
ax.scatter(np.full(6,2.),[.8,1.4,2.1,2.8,3.4,4.2],s=24,color=BLUE)
ax.axvline(2,color=GREY,linestyle=':',lw=1)
ax.text(2.18,3.8,r'对所有 $i$，$x_i=c$')
ax.text(.25,.3,r'$\beta_0+c\beta_1$：只能识别这一总和')
ax.set_xlim(0,4.3);ax.set_ylim(0,4.8);ax.set_xticks([0,2,4],['0','$c$','']);quiet(ax)
save(fig,'no_sample_variation')

fig, ax=plt.subplots(figsize=(6.2,3.1),layout='constrained')
grid=np.linspace(0,5,100);mean=lambda t:1+.7*t
ax.plot(grid,mean(grid),color=BLUE)
for xi,ui,label in [(1.3,-.7,'i'),(3.7,.9,'j')]:
    mu=mean(xi);yi=mu+ui
    ax.scatter([xi],[yi],color=BLUE,s=25)
    ax.scatter([xi],[mu],facecolors='white',edgecolors=BLUE,s=26,zorder=3)
    ax.vlines(xi,mu,yi,color=RED,lw=1.6)
    ax.text(xi+.12,(mu+yi)/2,f'$u_{label}$',color=RED,va='center')
    ax.text(xi-.13,yi+np.sign(ui)*.2,f'$y_{label}$',ha='right')
ax.text(.35,4.55,r'$E[y\mid x]=\beta_0+\beta_1x$',color=BLUE)
ax.set_xlim(0,5);ax.set_ylim(0,5);quiet(ax)
save(fig,'population_errors')

fig,ax=plt.subplots(figsize=(5.5,2.5),layout='constrained')
x=np.arange(1.,6.);y=.5+.8*x
ax.plot(x,y,color=GREY);ax.scatter(x,y,color=BLUE,s=22,zorder=3)
ax.text(1.3,3.7,r'$y_i=\hat y_i,\quad RSS=0,\quad R^2=1$',color=BLUE)
ax.set_xlim(.6,5.4);ax.set_ylim(.5,4.9);quiet(ax)
save(fig,'perfect_fit')

(OUT/'figure_statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(f'Generated 8 vector figures in {OUT}')
