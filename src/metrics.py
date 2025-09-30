# src/metrics.py
import numpy as np

def percent_error(pred, true):
    return 100.0 * np.abs(pred - true) / (np.abs(true) + 1e-9)

def combined_error(density_pred, density_true, rg_pred, rg_true, w_density=0.5, w_rg=0.5):
    e_density = percent_error(density_pred, density_true).mean()
    e_rg = percent_error(rg_pred, rg_true).mean()
    return w_density * e_density + w_rg * e_rg
