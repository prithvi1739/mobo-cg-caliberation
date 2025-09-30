# src/optimize.py
import optuna
from optuna.samplers import NSGAIISampler
import numpy as np
import os
import pandas as pd

from src.data import sample_polymer_design, ground_truth_model
from src.cg_model import cg_model, runtime_proxy
from src.metrics import combined_error

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# small dataset for calibration; change n for larger experiments
X = sample_polymer_design(n=50)
density_gt, rg_gt = ground_truth_model(X)

def objective(trial):
    s1 = trial.suggest_float('s1', 0.6, 1.4)
    s2 = trial.suggest_float('s2', 0.6, 1.4)
    s3 = trial.suggest_float('s3', 0.6, 1.4)
    c_scale = trial.suggest_float('c_scale', 0.5, 2.0)
    sb = trial.suggest_float('sb', -0.3, 0.3)

    theta = {'s1': s1, 's2': s2, 's3': s3, 'c_scale': c_scale, 'sb': sb}
    density_cg, rg_cg = cg_model(X, theta)
    err = combined_error(density_cg, density_gt, rg_cg, rg_gt)
    runtime = runtime_proxy(theta)
    return float(err), float(runtime)

def run_study(n_trials=200, save_csv=True):
    sampler = NSGAIISampler(seed=42)
    study = optuna.create_study(directions=['minimize', 'minimize'], sampler=sampler)
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    rows = []
    for t in study.trials:
        if t.values is None:
            continue
        row = dict(t.params)
        row['err'] = t.values[0]
        row['runtime'] = t.values[1]
        rows.append(row)
    df = pd.DataFrame(rows)
    if save_csv:
        csv_path = os.path.join(RESULTS_DIR, "study_results.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved results to {csv_path}")
    return study, df

if __name__ == "__main__":
    study, df = run_study(n_trials=200)
    print("Done. Top results (by error):")
    print(df.sort_values('err').head(10))