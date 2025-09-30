# src/data.py
import numpy as np

RNG = np.random.RandomState(42)

def sample_polymer_design(n=200, seed=42):
    """
    Each polymer represented by:
      - fractions of 3 monomer types (f1,f2,f3) that sum to 1
      - chain_length (scaled)
      - stiffness
    Returns design matrix X (n,5)
    """
    rng = np.random.RandomState(seed)
    f = rng.dirichlet([1.0, 1.0, 1.0], size=n)
    chain_len = rng.randint(50, 500, size=(n,1)) / 100.0  # scaled
    stiffness = rng.uniform(0.1, 2.0, size=(n,1))
    X = np.hstack([f, chain_len, stiffness])
    return X

def ground_truth_model(x):
    """
    Synthetic AAMD-like function.
    x: array of shape (5,) or (n,5)
    Returns density, Rg as numpy arrays (n,1)
    """
    x = np.atleast_2d(x)
    f1, f2, f3, chain_len, stiffness = x[:,0], x[:,1], x[:,2], x[:,3], x[:,4]
    density = 0.8 + 0.4*f1 + 0.15*np.sin(0.03*chain_len*100) + 0.05*f2*stiffness
    density += 0.02*np.sin(3.0*f3)
    rg = 0.2 * np.sqrt(chain_len * 100) * (1.0 + 0.3*stiffness) * (1 + 0.1*f3)
    return density.reshape(-1,1), rg.reshape(-1,1)
