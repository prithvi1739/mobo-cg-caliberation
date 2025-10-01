# AI-Optimized Polymer Simulation

### Multi-objective tuning of a coarse-grained (CG) model to match atomistic targets

## Overview

This project shows how a fast coarse-grained (CG) simulation can be calibrated to imitate a slower atomistic reference on two properties—density and radius of gyration (Rg)—while also keeping a runtime proxy low. The workflow uses multi-objective optimization to produce a Pareto front: the best speed/accuracy trade-offs.

## Why this is useful:

  - Atomistic models represent every atom. They’re accurate but slow.

  - Coarse-grained models group atoms into beads. They run much faster but start out biased.

  - By tuning a small set of CG parameters, we can approach atomistic accuracy at a fraction of the cost, which is ideal for screening many polymer candidates before any expensive, detailed runs.


## What’s in this repo:

<details>
<summary> Repo structure </summary>
 
```text
mobo-cg-calibration/
├─ src/
│  ├─ data.py        # synthetic polymer designs + synthetic atomistic reference
│  ├─ cg_model.py    # CG model + parameterization + runtime proxy
│  ├─ metrics.py     # % error and combined error
│  ├─ optimize.py    # NSGA-II optimization (Optuna)
│  └─ viz.py         # Pareto scatter plot
├─ notebooks/
│  └─ demo.ipynb     # click-through demo
├─ results/          # created at runtime: CSVs and plots
├─ README.md
└─ requirements.txt
```
</details>

## How it works:

  - Generate candidate polymers (monomer fractions, chain length, stiffness).

  - Compute the reference density and Rg with a synthetic atomistic-like function.

  - Predict with a fast CG model that has five tunable knobs (scales and a bias).

  - Score each setting on two objectives:

  - Combined percent error vs the reference (lower is better)

  - A runtime proxy (lower is better)

  - Search the parameter space with a multi-objective optimizer (NSGA-II).

  - Keep Pareto-optimal settings—you can’t improve speed and accuracy at the same time.

  - Pick a point on that front that fits your needs (for example, “error under 6% with very fast runtime”).

## Demo results (200-trial run):

  - Artifacts are written to results/.
  - CSV: results/study_results.csv

 | index | s1     | s2     | s3     | c_scale | sb      |  err (%) | runtime |
| ----: | :----- | :----- | :----- | :------ | :------ | -------: | ------: |
|    15 | 1.1832 | 1.2170 | 0.6592 | 1.0377  | −0.2305 | **3.97** |    9.71 |
|   117 | 1.1261 | 1.0546 | 0.6749 | 1.0516  | −0.2305 |     4.25 |    9.56 |
|    28 | 1.3700 | 0.8014 | 0.9978 | 0.9513  | −0.1291 |     4.30 |   10.57 |

| index | s1     | s2     | s3     | c_scale | sb      | err (%) |  runtime |
| ----: | :----- | :----- | :----- | :------ | :------ | ------: | -------: |
|    58 | 0.8794 | 0.6908 | 1.3398 | 1.9851  | −0.1452 |    5.11 | **5.11** |
|   147 | 0.8794 | 0.6908 | 0.6362 | 1.9851  | −0.0752 |    5.12 |     5.12 |
|   149 | 1.3427 | 0.9425 | 1.0198 | 1.9454  | 0.1256  |    5.18 |     5.18 |

## How to read the plot: 
  - The lower-left edge is the set of best trade-offs. Moving left favors speed; moving down favors accuracy.
 
 Plot: results/pareto.png
 <img width="873" height="710" alt="Screenshot 2025-09-30 215139" src="https://github.com/user-attachments/assets/407b8b6e-6ae7-425f-86eb-a605454dd285" />

## Quick start:
 Python 3.10+ recommended. Works with Conda or venv.
 ### Conda environment example:
```text
conda create -n mobo-cg python=3.10 -y
conda activate mobo-cg
pip install -r requirements.txt

# run optimization (writes results/study_results.csv)
python -m src.optimize

# make the Pareto plot (writes results/pareto.png)
python -c "from src.viz import plot_pareto; plot_pareto()"
```
## Interpreting the results:
  - Each dot is one parameter setting (θ).
  - Down = better accuracy. Left = faster/cheaper.
  - Choose a Pareto-optimal point that meets your accuracy target within your runtime budget, then validate with higher-fidelity or experimental data.
## What to tweak:
 * Weights (density vs Rg) in src/metrics.py.
 * Search ranges in src/optimize.py.
 * Dataset size in src/optimize.py (e.g., more designs for stability).
 * Optimizer choice (e.g., Bayesian multi-objective methods) if evaluations are costly.
 
## License:
MIT License © 2025 Prihvi krishna Alluri

This repository is an independent, educational demo inspired by the Multiscale Technologies polymer case study: https://multiscale.tech/casestudy-polymers/. It is not affiliated with or endorsed by Multiscale Technologies. No proprietary code or data from Multiscale is included. All trademarks and names are the property of their respective owners.

 
