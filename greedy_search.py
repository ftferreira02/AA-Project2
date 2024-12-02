import networkx as nx
import os
import time
from graph_utils import parse_graph_from_text, write_result_to_file, visualize_and_save_edge_dominating_set

# Define paths for storing results and images
GRAPH_TEXT_FILE = "Graphs/all_graphs_data.txt"
RESULT_TEXT_FILE = "Graphs/greedy_edge_dominating_sets.txt"
GREEDY_EDGE_DOMINATING_IMG_DIR = "Graphs/GreedySearchImages"

# Ensure the directory exists for saving images
os.makedirs(GREEDY_EDGE_DOMINATING_IMG_DIR, exist_ok=True)

def sorted_edge(u, v):
    """Return a tuple with the smaller node first."""
    return (u, v) if u <= v else (v, u)

def get_sorted_adjacent_edges(G, node):
    """Return a set of sorted edges adjacent to a node."""
    return set(sorted_edge(node, neighbor) for neighbor in G.neighbors(node))

def greedy_edge_dominating_set(G):
    """Find an edge dominating set using a greedy algorithm with consistent edge representation."""
    covered_edges = set()
    dominating_set = set()
    operation_count = 0
    
    start_time = time.time()
    
    # Ensure all edges are represented as sorted tuples
    all_edges = set(sorted_edge(u, v) for u, v in G.edges())
    
    while len(covered_edges) < len(all_edges):
        best_edge = None
        max_coverage = 0
        
        edges_to_consider = all_edges - covered_edges
        
        for edge in edges_to_consider:
            operation_count += 1
            u, v = edge
            adjacent_edges = get_sorted_adjacent_edges(G, u).union(get_sorted_adjacent_edges(G, v))
            # Include the edge itself
            adjacent_edges.add(edge)
            new_coverage = adjacent_edges - covered_edges
            coverage = len(new_coverage)
            
            if coverage > max_coverage:
                max_coverage = coverage
                best_edge = edge
                best_new_coverage = new_coverage
        
        if best_edge:
            dominating_set.add(best_edge)
            covered_edges.update(best_new_coverage)
        else:
            break  # No more edges to cover
    
    duration = time.time() - start_time
    return dominating_set, operation_count, duration


def main():
    # Clear the results file at the start
    with open(RESULT_TEXT_FILE, "w") as f:
        f.write("")  # Empty the file

    for G, graph_name, num_vertices, density in parse_graph_from_text(GRAPH_TEXT_FILE):
        print(f"Processing {graph_name} with {num_vertices} vertices and density {density}")
        
        edge_dominating_set, operation_count, duration = greedy_edge_dominating_set(G)
        
        # Visualize and save the graph image with the edge dominating set
        visualize_and_save_edge_dominating_set(
            G, edge_dominating_set, graph_name, GREEDY_EDGE_DOMINATING_IMG_DIR,
            title=f"Greedy Edge Dominating Set for {graph_name}", color="blue"
        )
        
        # Write the result immediately after finding it
        write_result_to_file(RESULT_TEXT_FILE, graph_name, edge_dominating_set, operation_count, duration)

if __name__ == "__main__":
    main()
