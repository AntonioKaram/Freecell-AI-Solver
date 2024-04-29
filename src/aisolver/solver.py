
from board import Board
from prioritqueue import PQAstar, PQBestFirst
from collections import deque

def heuristic_function(board: Board):
    empty_freecells=board.freecells.count(0)
    cards_in_foundations=sum([len([sublist for sublist in each_foundation])\
                                 for each_foundation in board.foundations])
    empty_stacks=sum([not stack for stack in board.stacks])

    return cards_in_foundations*60+empty_stacks*30+empty_freecells*10

class BFS:

    def __init__(self, start_board):
        self.start_board = start_board
        self.visited = set()
        self.nodes_visited = 0


    def search(self):
        queue = deque([(self.start_board, [])])
        
        while queue:
            (state,path) = queue.popleft()
            self.nodes_visited += 1

            for children in state._children():
                for node, move in children:
                    if node in self.visited:
                        continue
                    if node.goal():
                        print('Solved!', node)
                        yield path+[move]
                    else:
                        queue.append((node, path + [move]))
                        self.visited.add(node)

class DFS:

    def __init__(self, start_board):
        self.start_board = start_board
        self.nodes_visited = 0
        self.visited = deque([])

    def search(self, state=None, path=None):
        self.nodes_visited+=1
        self.visited+=[state]

        if not state and not path:
            state, path = self.start_board, []

        if state.goal():
            print('Solved!', state)
            yield path

        for children in state._children():
            for node, move in children:
                if node not in self.visited:
                    yield from self.search(node, path+[move])

class AStar:
    def __init__(self, start_board, heuristic=heuristic_function):
        self.start_board = start_board
        self.heuristic = heuristic
        self.visited = set()
        self.nodes_visited = 0

    def search(self):
        queue = PQAstar(self.heuristic)
        queue.put((self.start_board, []))

        while not queue.empty():
            state,path=queue.get() 
            self.nodes_visited+=1

            if state.goal():
                yield path

            for children in state._children():
                for node, move in children:
                    if node in self.visited:
                        continue
                    queue.put((node, path+[move]))
                    #print(node)
                    self.visited.add(node)

class BestFirst:
    def __init__(self, start_board, heuristic=heuristic_function):
        self.start_board = start_board
        self.heuristic = heuristic
        self.visited = set()
        self.nodes_visited = 0

    def search(self):
        queue = PQBestFirst(self.heuristic)
        queue.put((self.start_board, []))

        while not queue.empty():
            state,path=queue.get() 
            self.nodes_visited+=1

            if state.goal():
                #print('Solved!', node)
                #print('Total nodes visited: {}'.format(self.nodes_visited))
                yield path

            for children in state._children():
                for node, move in children:
                    if node in self.visited:
                        continue
                    queue.put((node, path+[move]))
                    #print(node)
                    self.visited.add(node)