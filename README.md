AI-Optimized Polymer Simulation

Multi-objective tuning of a coarse-grained (CG) model to match atomistic targets

Overview

This project shows how a fast coarse-grained (CG) simulation can be calibrated to imitate a slower atomistic reference on two properties—density and radius of gyration (Rg)—while also keeping a runtime proxy low.
The workflow uses multi-objective optimization to produce a Pareto front: the best speed/accuracy trade-offs.

Why this is useful

Atomistic models represent every atom. They’re accurate but slow.

Coarse-grained models group atoms into beads. They run much faster but start out biased.

By tuning a small set of CG parameters, we can get close to atomistic accuracy at a fraction of the cost, which is ideal for screening many polymer candidates before any expensive, detailed runs.

What’s in this repo
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

How it works (plain English)

Generate candidate polymers (monomer fractions, chain length, stiffness).

Compute the “reference” density and Rg with a synthetic atomistic-like function.

Predict with a fast CG model that has five tunable knobs (scales and a bias).

Score each setting on two objectives:

Combined percent error vs the reference (lower is better)

A runtime proxy (lower is better)

Search the parameter space with a multi-objective optimizer (NSGA-II).

Keep only Pareto-optimal settings—the ones you can’t improve on both speed and accuracy at the same time.

Pick a point on that front that fits your needs (for example, “error under 6% with very fast runtime”).

Demo results (one full run)

A 200-trial run produced the artifacts below.

CSV: results/study_results.csv — one row per trial (s1,s2,s3,c_scale,sb,err,runtime)

Plot: results/pareto.png — error (y) vs runtime proxy (x)

Best observed (by lowest error):

index	s1	s2	s3	c_scale	sb	err (%)	runtime
15	1.1832	1.2170	0.6592	1.0377	−0.2305	3.97	9.71
117	1.1261	1.0546	0.6749	1.0516	−0.2305	4.25	9.56
28	1.3700	0.8014	0.9978	0.9513	−0.1291	4.30	10.57

Very fast with low error (sorted by runtime):

index	s1	s2	s3	c_scale	sb	err (%)	runtime
58	0.8794	0.6908	1.3398	1.9851	−0.1452	5.11	5.11
147	0.8794	0.6908	0.6362	1.9851	−0.0752	5.12	5.12
149	1.3427	0.9425	1.0198	1.9454	0.1256	5.18	5.18

How to read this: the lower-left edge of results/pareto.png is the set of best trade-offs. Moving left favors speed; moving down favors accuracy.

Quick start

Python 3.10+ recommended. Works on Windows, macOS, Linux. Conda or venv are both fine.

# (Conda example)
conda create -n mobo-cg python=3.10 -y
conda activate mobo-cg

pip install -r requirements.txt

# run optimization (writes results/study_results.csv)
python -m src.optimize

# make the Pareto plot (writes results/pareto.png)
python -c "from src.viz import plot_pareto; plot_pareto()"

Interpreting the plot

Each dot is one parameter setting.

Down is better accuracy. Left is cheaper/faster.

Points along the lower-left boundary are Pareto-optimal—you can’t improve one objective without hurting the other.

Choose a point that meets your accuracy target within your runtime budget, then validate it with higher-fidelity or experimental data.

What to tweak:

Weights: Give density or Rg more weight in src/metrics.py if one matters more.

Parameter ranges: Narrow or widen the search ranges in src/optimize.py.

Data size: Increase the number of synthetic designs for a sturdier calibration.

Optimizer: Switch to a Bayesian multi-objective approach (e.g., BoTorch/Ax) if evaluations are very costly.

Notes for technical readers:

The atomistic “reference” is a synthetic function for reproducibility.

The runtime term is a proxy; in a real pipeline this would reflect wall-clock, GPU hours, queueing, or cost.

The CG model is intentionally biased; optimization learns compensating parameter settings that reduce error while controlling runtime.