import re
import pandas as pd

def parse_results_file(filename, algorithm):
    data = {
        "Graph": [],
        "Vertices": [],
        "Density": [],
        "Edge_Dominating_Set_Size": [],
        "Basic_Operations": [],
        "Time_Taken": [],
        "Algorithm": []
    }

    with open(filename, "r") as file:
        content = file.read().split("========================================\n")
        for entry in content:
            if entry.strip():
                # Extract data with regular expressions
                graph_name = re.search(r"Graph:\s+(.+)", entry)
                if graph_name:
                    graph_name = graph_name.group(1)
                else:
                    continue  # Skip entry if no graph name is found

                # Extract vertices from graph name
                vertices_match = re.search(r"graph_(\d+)_vertices", graph_name)
                vertices = int(vertices_match.group(1)) if vertices_match else None

                # Extract density from graph name
                density_match = re.search(r"(\d+)[_]?(pct_edges)", graph_name)
                density = int(density_match.group(1)) / 100 if density_match else None

                # Calculate the size of the edge dominating set
                edge_dominating_set_size = len(re.findall(r"\((\d+), (\d+)\)", entry))

                # Extract basic operations
                basic_operations_match = re.search(r"Basic Operations:\s+(\d+)", entry)
                basic_operations = int(basic_operations_match.group(1)) if basic_operations_match else 0

                # Extract time taken
                time_taken_match = re.search(r"Time Taken:\s+([\d.]+) seconds", entry)
                time_taken = float(time_taken_match.group(1)) if time_taken_match else 0.0

                # Append data to the dictionary
                data["Graph"].append(graph_name)
                data["Vertices"].append(vertices)
                data["Density"].append(density)
                data["Edge_Dominating_Set_Size"].append(edge_dominating_set_size)
                data["Basic_Operations"].append(basic_operations)
                data["Time_Taken"].append(time_taken)
                data["Algorithm"].append(algorithm)  # Add algorithm type (Greedy or Exhaustive)

    # Convert the dictionary to a DataFrame
    return pd.DataFrame(data)

# Usage
greedy_filename = "Graphs/greedy_edge_dominating_sets.txt"  # Replace with your actual greedy results file
exhaustive_filename = "Graphs/min_edge_dominating_sets.txt"  # Replace with your exhaustive results file

greedy_df = parse_results_file(greedy_filename, "Greedy")
exhaustive_df = parse_results_file(exhaustive_filename, "Exhaustive")

# Combine both DataFrames for comparison
results_df = pd.concat([greedy_df, exhaustive_df], ignore_index=True)
