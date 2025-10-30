import sys
from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

import networkx as nx

try:
    from practicum_4.dfs import GraphTraversal
    from src.plotting.graphs import plot_graph
    from src.common import AnyNxGraph
except ImportError:
    class GraphTraversal: pass
    class AnyNxGraph: pass
    def plot_graph(*args, **kwargs): pass

class DfsViaLifoQueueWithPostvisit:
    def __init__(self, G):
        self.G = G
        self.visited = set()
    
    def run(self, node: Any) -> None:
        stack = [(node, False)]  

        while stack:
            current, postvisit_flag = stack.pop()
            
            if postvisit_flag:
                self.postvisit(current)
                continue
                
            if current in self.visited:
                continue
                
            self.visited.add(current)
            self.previsit(current)
            
            stack.append((current, True))
            
            for neighbor in reversed(list(self.G.neighbors(current))):
                if neighbor not in self.visited:
                    stack.append((neighbor, False))
    
    def previsit(self, node: Any) -> None:
        pass
    
    def postvisit(self, node: Any) -> None:
        pass

class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any) -> None:
        print(f"Postvisit node {node}")

if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ('0', '1'), ('1', '2'), ('2', '3'), ('3', '4'),
        ('4', '5'), ('5', '6'), ('6', '7'), ('7', '8'), ('8', '9')
    ]
    G.add_edges_from(edges)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
