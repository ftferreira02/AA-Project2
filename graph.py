import networkx as nx
import numpy as np
import random
import math
import matplotlib.pyplot as plt  # For graph visualization
import os
from itertools import combinations
import shutil

# Seed for reproducibility (use your student number)
random.seed(124467)

# Define the directory to save the graphs
GRAPH_DIR = "Graphs"

GRAPH_DIR_IMG = "Graphs/Images"

RESULT_TEXT_FILE = os.path.join(GRAPH_DIR, "min_edge_dominating_sets.txt")

os.makedirs(GRAPH_DIR_IMG, exist_ok=True)  # Ensures the images directory exists

# Ensure the directory exists
os.makedirs(GRAPH_DIR, exist_ok=True)

# Define the single text file path for storing all graphs
GRAPH_TEXT_FILE = os.path.join(GRAPH_DIR, "all_graphs_data.txt")

def generate_vertex_coordinates(num_vertices, min_distance=10, coordinate_range=(1, 1000)):
    """Generate distinct vertex coordinates in 2D space with minimum distance constraints."""
    coordinates = np.empty((0, 2), int)
    while len(coordinates) < num_vertices:
        # Generate a candidate coordinate
        candidate = np.random.randint(coordinate_range[0], coordinate_range[1], size=2)
        # Calculate distances to existing coordinates
        if len(coordinates) == 0 or np.all(np.linalg.norm(coordinates - candidate, axis=1) >= min_distance):
            coordinates = np.vstack([coordinates, candidate])
    return [tuple(coord) for coord in coordinates]

def create_graph_with_density(num_vertices, density, min_distance=10):
    """Create a graph with a specified number of vertices and edge density."""
    G = nx.Graph()
    coordinates = generate_vertex_coordinates(num_vertices, min_distance)
    G.add_nodes_from((i, {"pos": coord}) for i, coord in enumerate(coordinates))

    possible_edges = list(combinations(range(num_vertices), 2))
    num_edges = int(density * len(possible_edges))
    G.add_edges_from(random.sample(possible_edges, num_edges))
    return G

def save_graph_as_image(graph, filename):
    """Save the graph visualization as a PNG image."""
    filepath = os.path.join(GRAPH_DIR_IMG, filename + ".png")
    pos = nx.get_node_attributes(graph, 'pos')  # Get node positions
    
    # Draw and save the graph as an image
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1500, font_size=15)
    plt.savefig(filepath, format="png")
    plt.close()  # Close the plot to free memory
    print(f"Graph image saved as: {filepath}")

def append_graph_to_text_file(graph, filename, num_vertices, density):
    with open(GRAPH_TEXT_FILE, "a") as f:
        f.write(f"Graph: {filename}\nVertices: {num_vertices}, Density: {density}\nNodes:\n")
        for node, pos in nx.get_node_attributes(graph, 'pos').items():
            f.write(f"{node} {pos[0]} {pos[1]}\n")
        f.write("Edges:\n")
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")
        f.write("\n" + "="*40 + "\n\n")
    print(f"Graph data appended to text file: {GRAPH_TEXT_FILE}")


def visualize_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1500, font_size=15)
    plt.show()

def log(message):
    print(message)

def clear_previous_data():
    """Clear the contents of the image directory and reset output files."""
    
    # Clear all files in the image directory
    if os.path.exists(GRAPH_DIR_IMG):
        for filename in os.listdir(GRAPH_DIR_IMG):
            file_path = os.path.join(GRAPH_DIR_IMG, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Delete the file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete the directory if there are subdirectories
                
    print("Cleared image directory.")

    # Reset the text files by overwriting them with empty content
    with open(GRAPH_TEXT_FILE, "w") as f:
        f.write("")
    with open(RESULT_TEXT_FILE, "w") as f:
        f.write("")

    print("Reset output text files.")

def main():
    clear_previous_data()  # Call this at the start to ensure a clean setup
    choice = input("Do you want to (1) create new graphs or (2) view an existing graph image? Enter 1 or 2: ")
    
    if choice == '1':
        densities = [0.125, 0.25, 0.5, 0.75]
        max_vertices = 18

        for num_vertices in range(10, max_vertices + 1):
            for density in densities:
                G = create_graph_with_density(num_vertices, density)
                
                # Define the filename and save the graph as an image
                filename = f"graph_{num_vertices}_vertices_{int(density*100)}pct_edges"
                save_graph_as_image(G, filename)
                append_graph_to_text_file(G, filename, num_vertices, density)

    elif choice == '2':
        log(f"Available image files in '{GRAPH_DIR_IMG}':")
        files = os.listdir(GRAPH_DIR_IMG)
        png_files = [f for f in files if f.endswith('.png')]
        
        if png_files:
            for i, file in enumerate(png_files, start=1):
                log(f"{i}. {file}")
            file_choice = int(input("Enter the number of the file you want to view: ")) - 1
            
            if 0 <= file_choice < len(png_files):
                filename = png_files[file_choice]
                img = plt.imread(os.path.join(GRAPH_DIR_IMG, filename))
                plt.imshow(img)
                plt.axis("off")
                plt.show()
            else:
                log("Invalid selection.")
        else:
            log("No PNG files found in the directory.")

if __name__ == "__main__":
    main()
