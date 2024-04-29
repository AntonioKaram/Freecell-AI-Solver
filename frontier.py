import time
import utils
import solution
from utils import Utils
from solution import Solution
from collections import defaultdict

class Frontier:
    def __init__(self):
        self.nodes = set()
        self.current_node = None

    def search(self, initial_state, method, output_file):
        initial_state.set_method(method)
        visited = set()
        solution_found = False
        start = time.time()
        time_elapsed = 0
        num_nodes_expanded = 0
        self.nodes.add(initial_state)

        print(f"Start searching using {method}...")

        while self.nodes and not solution_found and time_elapsed < Utils.LIMIT:
            self.current_node = min(self.nodes, key=lambda x: x.get_priority())
            
            if self.current_node in visited:
                continue
            
            visited.add(self.current_node)

            if self.current_node.is_solved():
                solution_found = True
                break
            else:
                children = self.current_node.get_children_of_state(method)
                for child in children:
                    if child not in visited:
                        self.nodes.add(child)

                num_nodes_expanded += 1

            if num_nodes_expanded % 2 == 0:
                time_elapsed = time.time() - start

        Solution(self.current_node, output_file, solution_found)

        print(f"Results: Solution found: {solution_found}, Time elapsed: {time_elapsed:.2f}s, "
              f"Nodes in frontier: {len(self.nodes)}, Nodes expanded: {num_nodes_expanded}, "
              f"Visited nodes: {len(visited)}")

        self.nodes = None
        self.current_node = None
