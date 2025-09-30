# src/viz.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_pareto(csv_path=os.path.join(RESULTS_DIR, "study_results.csv"), out_path=None):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(7,5))
    sns.scatterplot(data=df, x='runtime', y='err')
    plt.xlabel('Runtime proxy (lower better)')
    plt.ylabel('Combined % Error (lower better)')
    plt.title('Pareto samples: error vs runtime')
    plt.grid(True)
    if out_path is None:
        out_path = os.path.join(RESULTS_DIR, "pareto.png")
    plt.savefig(out_path, dpi=150)
    plt.show()
    print(f"Saved pareto plot to {out_path}")

def show_top_examples(csv_path=os.path.join(RESULTS_DIR, "study_results.csv"), top_n=3):
    df = pd.read_csv(csv_path)
    print("Top by lowest error:")
    display(df.sort_values('err').head(top_n))