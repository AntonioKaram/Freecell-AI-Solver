
from statistics import mean
from collections import deque
from aisolver.board import Board
from aisolver.prioritqueue import PQAstar, PQBestFirst

# Define a heuristic function to be used by A*
def heuristic_function(board: Board):
    distane_to_goal = sum([len([sublist for sublist in each_foundation]) for each_foundation in board.foundations])
    distance_from_top = mean([int(stack[-1][1:]) if stack else 0 for stack in board.stacks]) - mean([int(stack[-1][1:]) if stack else 0 for stack in board.foundations])

    lowest_foundation = 99
    for foundation in board.foundations:
        for card in foundation:
            lowest_foundation = min(lowest_foundation, int(card[1:]))
    lowest_home_card = board.MAX_CARD - lowest_foundation


    uppest_foundation = 0
    for foundation in board.foundations:
        for card in foundation:
            uppest_foundation = max(uppest_foundation, int(card[1:]))
            
            
    uppest_home_card = board.MAX_CARD - uppest_foundation


    difference_home = uppest_foundation - lowest_foundation
    bottom_cards_sum = (board.MAX_CARD * 4) - sum([int(stack[0][1:]) if stack else 0 for stack in board.stacks])

    return (distane_to_goal * 85) + (distance_from_top *7) + (uppest_home_card * 8)

class DFS:

    def __init__(self, start_board, max_iter=500000):
        self.start_board = start_board
        self.nodes_visited = 0
        self.max_iter = max_iter
        self.visited = deque([])

    def search(self, state=None, path=None):

        if self.nodes_visited >= self.max_iter:
            return
        self.nodes_visited+=1
        self.visited+=[state]

        if not state and not path:
            state, path = self.start_board, []

        if state.goal():
            yield path

        for children in state._children():
            for node, move in children:
                if node not in self.visited:
                    yield from self.search(node, path+[move])

class AStar:
    def __init__(self, start_board, heuristic=heuristic_function, max_iter = 500000):
        self.start_board = start_board
        self.heuristic = heuristic
        self.visited = set()
        self.max_iter = max_iter
        self.nodes_visited = 0

    def search(self):
        queue = PQAstar(self.heuristic)
        queue.put((self.start_board, []))

        while not queue.empty() and self.nodes_visited <= self.max_iter:
            state, path=queue.get() 
            self.nodes_visited+=1

            if state.goal():
                yield path

            for children in state._children():
                for node, move in children:
                    if node in self.visited:
                        continue
                    queue.put((node, path+[move]))
                    self.visited.add(node)

class BestFirst:
    def __init__(self, start_board, heuristic=heuristic_function, max_iter=500000):
        self.start_board = start_board
        self.heuristic = heuristic
        self.visited = set()
        self.nodes_visited = 0
        self.max_iter = max_iter

    def search(self):
        queue = PQBestFirst(self.heuristic)
        queue.put((self.start_board, []))

        while not queue.empty() and self.nodes_visited <= self.max_iter:
            state,path=queue.get() 
            self.nodes_visited+=1

            if state.goal():
                yield path

            for children in state._children():
                for node, move in children:
                    if node in self.visited:
                        continue
                    queue.put((node, path+[move]))
                    self.visited.add(node)
