"""Small, independent numerical checks of the mathematical claims and examples."""
from pathlib import Path
import json
import math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def main():
    results={}
    def close(name,a,b,tol=1e-10):
        err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        assert err<tol, (name,a,b,err)
        results[name]={'passed':True,'max_absolute_error':err}
    rng=np.random.default_rng(20261020)
    x=rng.normal(size=40);z=.7*x+rng.normal(size=40)
    y=1+2*x-.8*z+rng.normal(size=40)
    X=np.column_stack([np.ones(len(x)),x,z])
    beta=np.linalg.lstsq(X,y,rcond=None)[0];fit=X@beta;u=y-fit
    close('normal_equations',X.T@u,np.zeros(3))
    tss=np.sum((y-y.mean())**2);ess=np.sum((fit-y.mean())**2);rss=np.sum(u*u)
    close('tss_equals_ess_plus_rss',tss,ess+rss)
    close('r2_equals_squared_correlation',1-rss/tss,np.corrcoef(y,fit)[0,1]**2)
    W=X[:,[0,2]]
    rx=x-W@np.linalg.lstsq(W,x,rcond=None)[0]
    ry=y-W@np.linalg.lstsq(W,y,rcond=None)[0]
    close('fwl_one_sided_slope',np.dot(rx,y)/np.dot(rx,rx),beta[1])
    fwl=np.dot(rx,ry)/np.dot(rx,rx)
    close('fwl_two_sided_slope',fwl,beta[1])
    close('fwl_two_sided_residuals',ry-fwl*rx,u)
    A=X[:,:2]
    short=np.linalg.lstsq(A,y,rcond=None)[0]
    delta=np.linalg.lstsq(A,z,rcond=None)[0]
    close('short_long_exact_sample_identity',short[1],beta[1]+beta[2]*delta[1])
    xc=x-x.mean();yc=y-y.mean()
    close('demeaning_preserves_intercept_model_slope',np.dot(xc,yc)/np.dot(xc,xc),short[1])
    check=np.dot(x,y)/np.dot(x,x);urto=y-check*x
    close('rto_inner_product',np.dot(x,urto),0)
    close('rto_covariance',np.mean((x-x.mean())*(urto-urto.mean())),-x.mean()*urto.mean())
    # Exact conditional mean over a symmetric finite error distribution.
    btrue=np.array([.7,1.2,-.6]);noise=rng.normal(size=40)
    sampled=[X@btrue+noise,X@btrue-noise]
    meanshort=np.mean([np.linalg.lstsq(A,yy,rcond=None)[0][1] for yy in sampled])
    close('conditional_omitted_variable_bias',meanshort,btrue[1]+btrue[2]*delta[1])
    example={
      'wage12_thousands':-.9+.54*12,
      'wage16_thousands':-.9+.54*16,
      'anson_residual_thousands':.006-(-.9+.54*12),
      'anson_scenario_thousands':.006+.54*4,
      'vote_share_at_40':26.81+.464*40,
      'required_share_percent':(50-26.81)/.464,
      'gpa_anson':1.29+.453*3.5+.0094*30,
      'gpa_betty':1.29+.453*3+.0094*36,
      'gpa_increment':.453*.1,
      'adjusted_r2_one':1-140/139*(1-.172),
      'adjusted_r2_two':1-140/138*(1-.176),
      'exact_education_percentage':100*math.expm1(.092),
    }
    t=example['required_share_percent']
    example['required_A_billions']=2*t/(100-t)
    close('source_wage_arithmetic',example['anson_scenario_thousands'],2.166)
    close('source_vote_arithmetic',example['vote_share_at_40'],45.37)
    close('source_gpa_arithmetic',[example['gpa_anson'],example['gpa_betty'],example['gpa_increment']],[3.1575,2.9874,.0453])
    assert example['adjusted_r2_two']<example['adjusted_r2_one']
    # A counterexample to zero covariance implying zero conditional mean.
    xx=np.array([-1.,0.,1.]);uu=xx**2-2/3
    close('zero_covariance_counterexample',np.dot(xx,uu),0)
    assert np.any(np.abs(uu)>0)
    figures=json.loads((ROOT/'figures'/'figure_statistics.json').read_text())
    close('figure_r2_094',figures['r2_0.94'],.94)
    close('figure_r2_064',figures['r2_0.64'],.64)
    assert figures['through_origin']['centered_r2']<0
    results['example_values']=example
    results['figure_statistics']=figures
    (ROOT/'qa'/'math_verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Mathematical checks passed:',sum(isinstance(v,dict) and v.get('passed',False) for v in results.values()))

if __name__=='__main__':main()
