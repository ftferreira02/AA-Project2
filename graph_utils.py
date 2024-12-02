import networkx as nx
import os
import matplotlib.pyplot as plt

def parse_graph_from_text(file):
    """Parse graphs from a text file."""
    with open(file, "r") as f:
        G = None
        graph_name = ""
        num_vertices = 0
        density = 0.0
        reading_nodes = False
        reading_edges = False

        for line in f:
            line = line.strip()
            if line.startswith("Graph:"):
                if G is not None:
                    yield G, graph_name, num_vertices, density
                
                graph_name = line.split(":")[1].strip()
                G = nx.Graph()
                reading_nodes = reading_edges = False
            
            elif line.startswith("Vertices:"):
                num_vertices = int(line.split(",")[0].split(":")[1].strip())
                density = float(line.split(",")[1].split(":")[1].strip())

            elif line == "Nodes:":
                reading_nodes = True
                reading_edges = False
                continue

            elif line == "Edges:":
                reading_edges = True
                reading_nodes = False
                continue

            elif line.startswith("=") or not line:
                if G is not None:
                    yield G, graph_name, num_vertices, density
                    G = None
                reading_nodes = reading_edges = False

            elif reading_nodes and len(line.split()) == 3:
                node, x, y = line.split()
                G.add_node(int(node), pos=(float(x), float(y)))

            elif reading_edges and len(line.split()) == 2:
                u, v = map(int, line.split())
                G.add_edge(u, v)

        if G is not None:
            yield G, graph_name, num_vertices, density

def write_result_to_file(result_file, graph_name, edge_dominating_set, operation_count, duration, timed_out=False):
    """Write a single result to the results file in append mode, noting if a timeout occurred."""
    try:
        with open(result_file, "a") as f:
            f.write(f"Graph: {graph_name}\n")
            if timed_out:
                f.write("Result: Timed out after 2 minutes.\n")
            else:
                f.write(f"Edge Dominating Set: {sorted(edge_dominating_set)}\n")
                f.write(f"Basic Operations: {operation_count}\n")
                f.write(f"Time Taken: {duration:.4f} seconds\n")
            f.write("=" * 40 + "\n")
        print(f"Result for {graph_name} saved to {result_file}")
    except Exception as e:
        print(f"Error while writing to file: {e}")

def visualize_and_save_edge_dominating_set(G, edge_dominating_set, graph_name, img_dir, title, color="blue"):
    """Visualize and save the graph with highlighted edge dominating set."""
    pos = nx.get_node_attributes(G, 'pos')  # Position dictionary for nodes
    plt.figure(figsize=(8, 6))
    
    # Draw all edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="gray", alpha=0.5)
    # Draw edges in the edge dominating set with specified color
    nx.draw_networkx_edges(G, pos, edgelist=edge_dominating_set, edge_color=color, width=2.5)
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightgreen", node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    
    # Save the image
    filename = os.path.join(img_dir, f"{graph_name}_edge_dominating_set.png")
    plt.title(title)
    plt.savefig(filename)
    plt.close()
    print(f"Image saved: {filename}")
