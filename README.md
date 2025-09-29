# AI-Optimized Polymer Simulation: MOBO for Coarse-Grained Models  

> ⚠️ **Status**: Work in Progress  

This project demonstrates how **AI-powered multi-objective optimization** can accelerate scientific simulations by calibrating **coarse-grained (CG) polymer models** to match the accuracy of expensive **atomistic simulations (AAMD)**.  

Inspired by a case study from **Multiscale Technologies**, this work replicates the workflow of their **MIND platform** in a simplified, reproducible demo.  

---

## 🚀 The Problem  
- Atomistic Molecular Dynamics (AAMD) → **High accuracy, but 2–3 days per run**.  
- Coarse-Grained Molecular Dynamics (CGMD) → **Fast, but up to 60% error** when used for polymers.  
- R&D teams face a **speed vs accuracy tradeoff** that limits how many material candidates they can explore.  

---

## 💡 The Solution  
This repo implements a **Multi-Objective Bayesian Optimization (MOBO)** workflow that:  
1. Tunes CG model parameters (scaling factors, biases, coarsening levels).  
2. Minimizes error vs. ground truth (density, radius of gyration).  
3. Minimizes runtime cost (proxy for simulation time).  

The result is a **Pareto front of tradeoffs**: solutions where CG models are **both faster and more accurate** than naïve baselines.  

---

## 📊 Key Outcomes (Demo Goals)  
- Show **100x runtime speedup equivalents** in synthetic experiments.  
- Reduce error from ~60% baseline → **<10% after optimization** (mirroring Multiscale’s case study).  
- Visualize convergence, Pareto fronts, and calibrated models.  

---

