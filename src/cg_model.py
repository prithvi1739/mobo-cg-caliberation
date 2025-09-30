# src/cg_model.py
import numpy as np

def cg_transform_design(x, theta):
    """
    Apply CG parameterization to design x using theta.
    theta: dict with s1,s2,s3,c_scale,sb
    """
    x = np.atleast_2d(x)
    s1, s2, s3 = theta['s1'], theta['s2'], theta['s3']
    c_scale, sb = theta['c_scale'], theta['sb']
    f = x[:, :3].copy()
    f[:,0] *= s1
    f[:,1] *= s2
    f[:,2] *= s3
    # renormalize fractions
    f = f / (f.sum(axis=1, keepdims=True) + 1e-9)
    chain_len = x[:,3] * c_scale
    stiffness = x[:,4] + sb
    return np.hstack([f, chain_len.reshape(-1,1), stiffness.reshape(-1,1)])

def cg_model(x, theta):
    """
    Parameterized CG predictions; intentionally biased relative to GT.
    Returns density_cg, rg_cg (n,1)
    """
    tx = cg_transform_design(x, theta)
    f1, f2, f3, chain_len, stiffness = tx[:,0], tx[:,1], tx[:,2], tx[:,3], tx[:,4]
    density_cg = 0.75 + 0.35*f1 + 0.12*np.sin(0.03*chain_len*100) + 0.04*f2*stiffness
    density_cg += 0.01*np.sin(2.5*f3)
    rg_cg = 0.22 * np.sqrt(chain_len * 100) * (1.0 + 0.25*stiffness) * (1 + 0.07*f3)
    return density_cg.reshape(-1,1), rg_cg.reshape(-1,1)

def runtime_proxy(theta):
    """
    Proxy for simulation runtime: smaller c_scale -> faster (smaller runtime value).
    """
    base = 10.0
    complexity_penalty = 0.1*(abs(theta['s1']-1)+abs(theta['s2']-1)+abs(theta['s3']-1))
    return base * (1.0 / theta['c_scale']) + complexity_penalty
