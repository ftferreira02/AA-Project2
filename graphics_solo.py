import re
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
from pandas_transformations import greedy_df, exhaustive_df, results_df

# Define a directory to store the plots
PLOT_DIR = "Plots"
os.makedirs(PLOT_DIR, exist_ok=True)  # Ensure the directory exists

# 1. Comparison of Execution Time for each graph
def plot_execution_time_log_scale(df, search):
    plt.figure(figsize=(12, 6))
    plt.bar(df["Graph"], df["Time_Taken"], color="skyblue")
    plt.xlabel("Graph")
    plt.ylabel("Time Taken (seconds, log scale)")
    plt.title(f"Execution Time for Each Graph ({search})")
    plt.yscale("log")  # Set y-axis to logarithmic scale
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f"execution_time_{search}_log.png"))
    plt.show()


# # 2. Basic Operations Count
# def plot_basic_operations(df, search):
#     plt.figure(figsize=(12, 6))
#     plt.bar(df["Graph"], df["Basic_Operations"], color="salmon")
#     plt.xlabel("Graph")
#     plt.ylabel("Basic Operations")
#     plt.title("Basic Operations Count for Each Graph")
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(os.path.join(PLOT_DIR, f"basic_operations{search}.png"))  # Save as PNG

def plot_basic_operations_bar_chart_log(df , search):
    # Set up the style
    plt.figure(figsize=(14, 6))
    
    # Plotting a bar chart with a logarithmic y-scale
    plt.bar(df['Graph'], df['Basic_Operations'], color='salmon', alpha=0.7)

    # Set labels, title, and adjust the y-scale
    plt.xlabel('Graph')
    plt.ylabel('Basic Operations [Log Scale]')
    plt.yscale('log')  # Use a logarithmic scale for the y-axis
    plt.title('Basic Operations Count for Each Graph')
    plt.xticks(rotation=90, ha='right', fontsize=8)  # Rotate x-tick labels for better visibility
    
    # Save the plot to file
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f"basic_operations{search}.png"))
    plt.show()


# 3. Solution Quality Comparison
def plot_solution_quality(df, search):
    plt.figure(figsize=(12, 6))
    plt.bar(df["Graph"], df["Edge_Dominating_Set_Size"], color="lightgreen")
    plt.xlabel("Graph")
    plt.ylabel("Edge Dominating Set Size")
    plt.title("Edge Dominating Set Size for Each Graph")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f"solution_quality{search}.png"))   # Save as PNG

# 4. Execution Time vs. Graph Density
def plot_time_vs_density(df, search):
    plt.figure(figsize=(8, 6))
    plt.scatter(df["Density"], df["Time_Taken"], color="purple")
    plt.xlabel("Graph Density")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Execution Time vs. Graph Density")
    plt.grid()
    plt.savefig(os.path.join(PLOT_DIR, f"time_vs_density{search}.png"))   # Save as PNG

# 5. Execution Time vs. Number of Vertices
def plot_time_vs_vertices(df, search):
    plt.figure(figsize=(8, 6))
    plt.scatter(df["Vertices"], df["Time_Taken"], color="orange")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Execution Time vs. Number of Vertices")
    plt.grid()
    plt.savefig(os.path.join(PLOT_DIR, f"time_vs_vertices{search}.png"))  # Save as PNG

def plot_basic_operations_vs_vertices(df,search):
    # Set up the style and colors
    sns.set_style("whitegrid")
    markers = ['+', 'o', 'x', 'v']  # Markers for different densities
    palette = sns.color_palette("Set1")

    plt.figure(figsize=(10, 6))

    # Loop over unique densities in the dataframe
    densities = df["Density"].unique()
    for i, density in enumerate(densities):
        # Subset the dataframe by density
        subset = df[df["Density"] == density]
        
        # Plot the basic operations vs number of vertices for each density
        plt.scatter(
            subset["Vertices"],
            subset["Basic_Operations"],
            label=f'Percentage max num edges {density}',
            alpha=0.7,
            marker=markers[i % len(markers)],
            color=palette[i % len(palette)]
        )
        
        # Fit a polynomial trend line to the data to show the tendency
        z = np.polyfit(subset["Vertices"], subset["Basic_Operations"], 2)  # Quadratic fit
        p = np.poly1d(z)
        plt.plot(subset["Vertices"], p(subset["Vertices"]), color=palette[i % len(palette)], linewidth=2)

    # Set labels, title, and legend
    plt.xlabel("Vertices Number")
    plt.ylabel("Number of Basic Operations")
    plt.title(f"Number of Basic Operations for Each Experiment with {search}")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"Plots/basic_operations_vs_vertices_trend{search}.png")
    plt.show()

def plot_basic_operations_vs_vertices_fixed(df, search):
    # Set up the style and colors
    sns.set_style("whitegrid")
    markers = ['+', 'o', 'x', 'v']  # Markers for different densities
    palette = sns.color_palette("Set1")

    plt.figure(figsize=(10, 6))

    # Loop over unique densities in the dataframe
    densities = df["Density"].unique()

    for i, density in enumerate(densities):
        # Subset the dataframe by density and filter out rows with zero or negative operations
        subset = df[(df["Density"] == density) & (df["Basic_Operations"] > 0)]
        
        # If subset is empty, skip this density
        if subset.empty:
            continue
        
        # Plot the basic operations vs number of vertices for each density
        plt.scatter(
            subset["Vertices"],
            subset["Basic_Operations"],
            label=f'Percentage max num edges {density}',
            alpha=0.7,
            marker=markers[i % len(markers)],
            color=palette[i % len(palette)]
        )
        
        # Fit a linear trend line to the data to show the tendency
        z = np.polyfit(subset["Vertices"], subset["Basic_Operations"], 1)  # Linear fit
        p = np.poly1d(z)
        plt.plot(subset["Vertices"], p(subset["Vertices"]), color=palette[i % len(palette)], linewidth=2)

    # Set labels, title, and legend
    plt.xlabel("Vertices Number")
    plt.ylabel("Number of Basic Operations [Log Scale]")
    plt.yscale('log')  # Use a logarithmic scale for better visualization
    plt.title(f"Number of Basic Operations for Each Experiment with {search}")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"Plots/basic_operations_vs_vertices_trend{search}.png")
    plt.show()


def generate_graphics_single(df, search):
    # plot_execution_time_log_scale(df , search)
    # plot_basic_operations(df, search)
    # plot_solution_quality(df, search)
    # plot_time_vs_density(df, search)
    # plot_time_vs_vertices(df, search)
    # Call the function using your DataFrame
    plot_basic_operations_vs_vertices(df,search)   


def main():
    generate_graphics_single(exhaustive_df, "exaustive")
    generate_graphics_single(greedy_df, "greedy")
    plot_basic_operations_bar_chart_log(exhaustive_df, "exaustive") 

if __name__ == "__main__":
    main()
