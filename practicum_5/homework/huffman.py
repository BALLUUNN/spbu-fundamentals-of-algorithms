from pathlib import Path
import heapq
from typing import Any, Union
from abc import ABC, abstractmethod
from collections import Counter, deque

import sys
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.tree: Union[None, tuple] = None
        self.codes: Union[None, dict] = None

    def _build_tree(self, sequence: list[Any]) -> None:
        frequency = Counter(sequence)
        priority_queue = [[freq, i, [sym, ""]] for i, (sym, freq) in enumerate(frequency.items())]
        heapq.heapify(priority_queue)
        
        uid = len(priority_queue)
        while len(priority_queue) > 1:
            lo = heapq.heappop(priority_queue)
            hi = heapq.heappop(priority_queue)
            for pair in lo[2:]:
                pair[1] = '0' + pair[1]
            for pair in hi[2:]:
                pair[1] = '1' + pair[1]
            
            merged_node = [lo[0] + hi[0], uid, *lo[2:], *hi[2:]]
            uid += 1
            heapq.heappush(priority_queue, merged_node)
        
        self.tree = priority_queue[0] if priority_queue else None

    def _generate_codes(self) -> None:
        if self.tree is None:
            self.codes = {}
            return
        self.codes = {sym: code for sym, code in self.tree[2:]}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""
            
        self._build_tree(sequence)
        self._generate_codes()
        
        if self.codes is None:
            return ""

        return "".join([self.codes[s] for s in sequence])

    def decode(self, encoded_sequence: str) -> list[Any]:
        if not encoded_sequence or self.tree is None:
            return []
        
        reverse_codes = {code: sym for sym, code in self.codes.items()}
        decoded_sequence = []
        current_code = ""
        for bit in encoded_sequence:
            current_code += bit
            if current_code in reverse_codes:
                decoded_sequence.append(reverse_codes[current_code])
                current_code = ""
        return decoded_sequence


class LossyCompression:
    def __init__(self) -> None:
        self.huffman_coder = HuffmanCoding()
        self.min_val: float = 0.0
        self.step: float = 1.0
        self.num_levels: int = 64 

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_val = np.min(time_series)
        max_val = np.max(time_series)
        self.step = (max_val - self.min_val) / (self.num_levels - 1)

        quantized_ts = np.round((time_series - self.min_val) / self.step).astype(int)
        
        return self.huffman_coder.encode(list(quantized_ts))

    def decompress(self, bits: str) -> NDArrayFloat:
        quantized_ts = self.huffman_coder.decode(bits)
        
        decompressed_ts = (np.array(quantized_ts) * self.step) + self.min_val
        return decompressed_ts


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")
