from pathlib import Path
from typing import Any, Dict, List, Tuple
import heapq
import networkx as nx
# from src.plotting.graphs import plot_graph


class ShortestPathFinder:

    
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self.distance_table: Dict[Any, float] = {}
        self.optimal_routes: Dict[Any, List[Any]] = {}
    
    def compute_shortest_paths(self, starting_node: Any) -> None:

        self.distance_table = {node: float('inf') for node in self.graph.nodes()}
        self.distance_table[starting_node] = 0
        
        self.optimal_routes = {starting_node: [starting_node]}
        
        priority_queue = [(0, starting_node)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_distance > self.distance_table[current_node]:
                continue
            
            for neighbor in self.graph.neighbors(current_node):
                edge_weight = self.graph.edges[current_node, neighbor].get('weight', 1.0)
                new_distance = current_distance + edge_weight
                
                if new_distance < self.distance_table[neighbor]:
                    self.distance_table[neighbor] = new_distance
                    self.optimal_routes[neighbor] = (
                        self.optimal_routes[current_node] + [neighbor]
                    )
                    heapq.heappush(priority_queue, (new_distance, neighbor))
    
    def get_shortest_distance(self, target_node: Any) -> float:
        return self.distance_table.get(target_node, float('inf'))
    
    def get_shortest_path(self, target_node: Any) -> List[Any]:
        return self.optimal_routes.get(target_node, [])
    
    def get_path_edges(self, target_node: Any) -> List[Tuple[Any, Any]]:

        path = self.get_shortest_path(target_node)
        return [
            (path[i], path[i + 1]) 
            for i in range(len(path) - 1)
        ]


def create_sample_graph() -> nx.Graph:

    sample_graph = nx.Graph()
    weighted_edges = [
        ('0', '1', 4), ('1', '2', 8), ('2', '3', 7), ('3', '4', 9),
        ('4', '5', 10), ('5', '6', 2), ('6', '7', 1), ('7', '0', 8),
        ('1', '7', 11), ('2', '8', 2), ('7', '8', 7), ('6', '8', 6),
        ('2', '5', 4), ('3', '5', 14)
    ]
    
    for u, v, weight in weighted_edges:
        sample_graph.add_edge(u, v, weight=weight)
    
    return sample_graph


if __name__ == "__main__":
    try:
        graph_data = nx.read_edgelist(
            Path("..") / "simple_weighted_graph_9_nodes.edgelist",
            create_using=nx.Graph
        )
    except FileNotFoundError:
        print("Файл графа не найден, используется пример графа")
        graph_data = create_sample_graph()
    
    # plot_graph(graph_data)
    
    path_finder = ShortestPathFinder(graph_data)
    path_finder.compute_shortest_paths("0")
    
    demonstration_node = "1"
    
    print(f"Кратчайшее расстояние до вершины {demonstration_node}: "
          f"{path_finder.get_shortest_distance(demonstration_node)}")
    
    print(f"Кратчайший путь до вершины {demonstration_node}: "
          f"{' -> '.join(path_finder.get_shortest_path(demonstration_node))}")
    
    highlighted_edges = path_finder.get_path_edges(demonstration_node)
    # plot_graph(graph_data, highlighted_edges=highlighted_edges)
