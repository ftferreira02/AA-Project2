import networkx as nx
import os
import time
import multiprocessing
from itertools import combinations
from graph_utils import parse_graph_from_text, write_result_to_file, visualize_and_save_edge_dominating_set

TIMEOUT = 240  # Timeout in seconds (2 minutes)
GRAPH_TEXT_FILE = "Graphs/all_graphs_data.txt"
RESULT_TEXT_FILE = "Graphs/min_edge_dominating_sets.txt"
MIN_EDGE_DOMINATING_IMG_DIR = "Graphs/ExaustiveSearchImages"

# Ensure the directory exists
os.makedirs(MIN_EDGE_DOMINATING_IMG_DIR, exist_ok=True)

def sorted_edge(u, v):
    """Return a tuple with the smaller node first."""
    return (u, v) if u <= v else (v, u)

def get_sorted_adjacent_edges(G, node):
    """Return a set of sorted edges adjacent to a node."""
    return set(sorted_edge(node, neighbor) for neighbor in G.neighbors(node))


def is_edge_dominating_set(G, edge_subset, all_edges):
    """Check if the edge_subset is an edge dominating set of G."""
    # Use sorted edges for consistent representation
    edge_subset = set(sorted_edge(u, v) for u, v in edge_subset)
    all_edges = set(sorted_edge(u, v) for u, v in all_edges)
    
    for edge in all_edges - edge_subset:
        u, v = edge
        # Check if edge is adjacent to any edge in edge_subset
        if not any(u in e or v in e for e in edge_subset):
            return False
    return True

def minimum_edge_dominating_set_with_timeout(G, timeout=TIMEOUT):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=minimum_edge_dominating_set_process, args=(G, result_queue))
    
    start_time = time.time()
    process.start()
    process.join()
    
    # if process.is_alive():
    #     process.terminate()
    #     process.join()
    #     return None, 0, time.time() - start_time, True
    # else:
    min_set, operation_count = result_queue.get()
    duration = time.time() - start_time
    return min_set, operation_count, duration, False

def minimum_edge_dominating_set_process(G, result_queue):
    all_edges = set(sorted_edge(u, v) for u, v in G.edges())
    min_dominating_set = None
    operation_count = 0

    for size in range(1, len(all_edges) + 1):
        found = False
        for edge_subset in combinations(all_edges, size):
            operation_count += 1
            edge_subset_set = set(edge_subset)
            
            if is_edge_dominating_set(G, edge_subset_set, all_edges):
                min_dominating_set = edge_subset_set
                found = True
                break  # Found a minimal set of current size

        if found:
            break  # No need to check larger sizes

    result_queue.put((min_dominating_set, operation_count))

def main():
    with open(RESULT_TEXT_FILE, "w") as f:
        f.write("")

    for G, graph_name, num_vertices, density in parse_graph_from_text(GRAPH_TEXT_FILE):
        print(f"Processing {graph_name} with {num_vertices} vertices and density {density}")
        
        min_edge_dominating_set, operation_count, duration, timed_out = minimum_edge_dominating_set_with_timeout(G)
        
        if not timed_out and min_edge_dominating_set:
            visualize_and_save_edge_dominating_set(
                G, min_edge_dominating_set, graph_name, MIN_EDGE_DOMINATING_IMG_DIR,
                title=f"Minimum Edge Dominating Set for {graph_name}", color="red"
            )
        
        write_result_to_file(RESULT_TEXT_FILE, graph_name, min_edge_dominating_set, operation_count, duration, timed_out)

if __name__ == "__main__":
    main()
