from typing import Any, Protocol
from itertools import combinations
from collections import deque
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 


class CentralityMeasure(Protocol):
    def __call__(self, G: nx.Graph) -> dict[Any, float]:
        ...


def plot_graph(G: nx.Graph, node_weights: dict[Any, float], figsize=(14, 8), name: str = ""):
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=42)
    
    nodes = nx.draw_networkx_nodes(
        G, pos,
        node_color=list(node_weights.values()),
        cmap=plt.cm.viridis,
        node_size=500,
        alpha=0.8
    )
    
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    
    plt.colorbar(nodes)
    plt.title(f"{name} Centrality")
    plt.axis("off")
    plt.show()


def create_custom_graph():
    G = nx.Graph()
    
    G.add_nodes_from(range(1, 16))

    edges = [
        (1, 2), (1, 3), (2, 3), (2, 4), (3, 5),
        (4, 5), (4, 6), (5, 7), (6, 7), (6, 8),
        (7, 9), (8, 9), (8, 10), (9, 11), (10, 11),
        (10, 12), (11, 13), (12, 13), (12, 14), (13, 15), (14, 15)
    ]
    G.add_edges_from(edges)
    
    return G
    

def closeness_centrality(G: nx.Graph) -> dict[Any, float]:  
    centrality_values = {}
    
    for node in G.nodes():
        distances = nx.shortest_path_length(G, source=node)
        total_distance = sum(dist for target, dist in distances.items() if target != node)
        
        reachable_nodes = len(distances) - 1
        if total_distance > 0 and reachable_nodes > 0:
            centrality_values[node] = reachable_nodes / total_distance
        else:
            centrality_values[node] = 0.0
            
    return centrality_values


def betweenness_centrality(G: nx.Graph) -> dict[Any, float]: 
    centrality_scores = {node: 0.0 for node in G.nodes()}
    all_nodes = list(G.nodes())
    
    for source_node in all_nodes:
        shortest_path_counts = {node: 0 for node in all_nodes}
        shortest_path_counts[source_node] = 1
        distances = {node: -1 for node in all_nodes}
        distances[source_node] = 0
        predecessors = {node: [] for node in all_nodes}
        
        queue = deque([source_node])
        visited_order = []
        
        while queue:
            current = queue.popleft()
            visited_order.append(current)
            
            for neighbor in G.neighbors(current):
                if distances[neighbor] < 0:
                    queue.append(neighbor)
                    distances[neighbor] = distances[current] + 1
                
                if distances[neighbor] == distances[current] + 1:
                    shortest_path_counts[neighbor] += shortest_path_counts[current]
                    predecessors[neighbor].append(current)
        
        node_dependencies = {node: 0 for node in all_nodes}
        while visited_order:
            current = visited_order.pop()
            for pred in predecessors[current]:
                if shortest_path_counts[current] > 0:
                    ratio = shortest_path_counts[pred] / shortest_path_counts[current]
                    node_dependencies[pred] += ratio * (1 + node_dependencies[current])
            
            if current != source_node:
                centrality_scores[current] += node_dependencies[current]
    
    return centrality_scores


def eigenvector_centrality(G: nx.Graph) -> dict[Any, float]:  
    nodes = list(G.nodes())
    A = nx.to_numpy_array(G, nodelist=nodes)
    
    eigenvalues, eigenvectors = np.linalg.eig(A)
    
    idx = np.argmax(eigenvalues)
    principal_vector = eigenvectors[:, idx].real
    
    if np.linalg.norm(principal_vector) > 0:
        principal_vector = principal_vector / np.linalg.norm(principal_vector)
    
    return {node: principal_vector[i] for i, node in enumerate(nodes)}


def plot_centrality_measure(G: nx.Graph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, name=measure.__name__)
    else:
        print(f"Реализуйте функцию {measure.__name__}")


if __name__ == "__main__":
    G = create_custom_graph()
    
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
