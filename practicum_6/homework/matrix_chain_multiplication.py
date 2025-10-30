from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class MatrixChainMultiplication:
    def __init__(self) -> None:
        pass

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[nx.Graph, Any]:
        n = len(matrices)
        dims = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]
        
        cost = np.zeros((n, n))
        split = np.zeros((n, n), dtype=int)
        
        for length in range(2, n+1):
            for i in range(n - length + 1):
                j = i + length - 1
                cost[i][j] = float('inf')
                for k in range(i, j):
                    current_cost = (cost[i][k] + cost[k+1][j] + 
                                   dims[i] * dims[k+1] * dims[j+1])
                    if current_cost < cost[i][j]:
                        cost[i][j] = current_cost
                        split[i][j] = k
        
        graph = nx.DiGraph()
        node_counter = 0
        
        def build_tree(i, j):
            nonlocal node_counter
            if i == j:
                name = matrices[i]["matrix_name"]
                graph.add_node(name)
                return name
            
            k = split[i][j]
            node_name = f"node_{node_counter}"
            node_counter += 1
            graph.add_node(node_name)
            
            left_child = build_tree(i, k)
            right_child = build_tree(k+1, j)
            
            graph.add_edge(node_name, left_child)
            graph.add_edge(node_name, right_child)
            
            return node_name
        
        root = build_tree(0, n-1)
        return graph, root


def plot_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10)
    plt.show()


if __name__ == "__main__":
    test_matrices = [
        {
            "matrix_name": "A",
            "shape": (2, 3),
        },
        {
            "matrix_name": "B",
            "shape": (3, 10),
        },
        {
            "matrix_name": "C",
            "shape": (10, 20),
        },
        {
            "matrix_name": "D",
            "shape": (20, 3),
        },
    ]

    mcm = MatrixChainMultiplication()
    matmul_tree, root = mcm.run(test_matrices)

    plot_graph(matmul_tree)
