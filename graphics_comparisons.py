import matplotlib.pyplot as plt
from pandas_transformations import results_df
import numpy as np
    
def plot_execution_time_comparison(df):
    plt.figure(figsize=(14, 7))
    algorithms = df["Algorithm"].unique()
    graphs = df["Graph"].unique()
    x = np.arange(len(graphs))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 7))
    bars = {}

    for i, algorithm in enumerate(algorithms):
        subset = df[df["Algorithm"] == algorithm]
        subset = subset.set_index("Graph").reindex(graphs)
        times = subset["Time_Taken"].values
        times = np.nan_to_num(times, nan=0)
        # Use log scale for time, adding a small value to avoid log(0)
        times = times + 1e-6
        bars[algorithm] = ax.bar(x + i * width, times, width, label=algorithm, alpha=0.7)

    ax.set_xlabel("Graph")
    ax.set_ylabel("Time Taken (seconds) [Log Scale]")
    ax.set_title("Execution Time Comparison: Greedy vs. Exhaustive")
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(graphs, rotation=45, ha="right")
    ax.set_yscale('log')  # Set y-axis to logarithmic scale
    ax.legend()

    plt.tight_layout()
    plt.savefig("Plots/execution_time_comparison_log_scale.png")
    plt.show()

def plot_basic_operations_comparison(df):
    plt.figure(figsize=(14, 7))
    algorithms = df["Algorithm"].unique()
    graphs = df["Graph"].unique()
    x = np.arange(len(graphs))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 7))
    bars = {}

    for i, algorithm in enumerate(algorithms):
        subset = df[df["Algorithm"] == algorithm]
        subset = subset.set_index("Graph").reindex(graphs)
        operations = subset["Basic_Operations"].values
        operations = np.nan_to_num(operations, nan=0)
        # Add a small value to avoid log(0)
        operations = operations + 1e-6
        bars[algorithm] = ax.bar(x + i * width, operations, width, label=algorithm, alpha=0.7)

    ax.set_xlabel("Graph")
    ax.set_ylabel("Basic Operations [Log Scale]")
    ax.set_title("Basic Operations Comparison: Greedy vs. Exhaustive")
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(graphs, rotation=45, ha="right")
    ax.set_yscale('log')  # Set y-axis to logarithmic scale
    ax.legend()

    # Optionally, add data labels
    for algorithm in algorithms:
        for bar in bars[algorithm]:
            yval = bar.get_height()
            if yval > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval,
                    f'{int(yval)}',
                    ha='center',
                    va='bottom',
                    fontsize=8,
                    rotation=90 if yval > 3 else 0,
                    color='red' if yval > 60 else 'black'
                )

    plt.tight_layout()
    plt.savefig("Plots/basic_operations_comparison_log_scale.png")
    plt.show()


def plot_solution_quality_comparison(df):
    plt.figure(figsize=(12, 6))
    for algorithm in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algorithm]
        plt.bar(subset["Graph"], subset["Edge_Dominating_Set_Size"], label=algorithm, alpha=0.7)
    plt.xlabel("Graph")
    plt.ylabel("Edge Dominating Set Size")
    plt.title("Edge Dominating Set Size Comparison: Greedy vs. Exhaustive")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Plots/solution_quality_comparison.png")
    plt.show()

def plot_time_vs_density_comparison(df):
    plt.figure(figsize=(10, 6))
    algorithms = df["Algorithm"].unique()

    for algorithm in algorithms:
        subset = df[df["Algorithm"] == algorithm]
        times = subset["Time_Taken"] + 1e-6  # Avoid log(0)
        plt.scatter(subset["Density"], times, label=algorithm, alpha=0.7)

    plt.xlabel("Graph Density")
    plt.ylabel("Time Taken (seconds) [Log Scale]")
    plt.title("Execution Time vs. Graph Density")
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("Plots/time_vs_density_comparison_log_scale.png")
    plt.show()


def plot_time_vs_vertices_comparison(df):
    plt.figure(figsize=(10, 6))
    algorithms = df["Algorithm"].unique()

    for algorithm in algorithms:
        subset = df[df["Algorithm"] == algorithm]
        times = subset["Time_Taken"] + 1e-6  # Avoid log(0)
        plt.scatter(subset["Vertices"], times, label=algorithm, alpha=0.7)

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time Taken (seconds) [Log Scale]")
    plt.title("Execution Time vs. Number of Vertices")
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("Plots/time_vs_vertices_comparison_log_scale.png")
    plt.show()

plot_execution_time_comparison(results_df)
plot_basic_operations_comparison(results_df)
plot_solution_quality_comparison(results_df)
plot_time_vs_density_comparison(results_df)
plot_time_vs_vertices_comparison(results_df)
