import copy
import heapq
from collections import deque

class Board:
    
    # Constant highest card
    MAX_CARD = 13

    def __init__(self, board):
        self.board = tuple(board)
        self.stacks = board[0]
        self.freecells = board[1]
        self.foundations = board[2]

    # Override string declaration
    def __str__(self):
        return '{}'.format(self.board)

    def __key(self):
        t_stacks = tuple(tuple(s) for s in self.stacks if s!=[])
        st_stacks = tuple(sorted(t_stacks, key=lambda item:item[-1]))
        t_freecells = tuple(filter(lambda item:item!=0, self.freecells))
        st_freecells = tuple(sorted(t_freecells, key=lambda item:item[:]))
        t_foundations = tuple(tuple(f) for f in self.foundations)
        return (st_stacks, st_freecells, t_foundations)

    # Override hash declaration
    def __hash__(self):
        return hash(self.__key())

    # Override equality declaration
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__key()==other.__key()

    @classmethod
    def new_board(cls, board):
        return Board(copy.deepcopy(board))
    
    def card_index(self, card):
        if card in self.freecells:
            return ('freecells', self.freecells.index(card))
        else:
            return ('stacks', next((i for i,stack in enumerate(self.stacks) if card in stack),None))

    def remove(self, card):
        (place, idx) = self.card_index(card)
        if place=='freecells':
            self.freecells[idx]=0
        else:
            self.stacks[idx].pop()

    @staticmethod
    def move_to_stack_requirements(card, other_card):
        suit, other_suit, value, other_value = 1 if card[0] in ('H','D') else 0,\
                1 if other_card[0] in ('H','D') else 0,int(card[1:]),int(other_card[1:])

        if suit==other_suit:
            return False
        elif suit!=other_suit and value==other_value-1:
            return True
        else:
            return False
    
    def goal(self):
        done = 0
        for idx,suit in zip(range(4),('H','D','S','C')):
            if self.foundations[idx] and self.foundations[idx][-1]==suit+str(self.MAX_CARD):
                done+=1
        return True if done==4 else False

    def move_to_freecell(self, card):
        return next((idx for idx,val in enumerate(self.freecells) if not val),None)

    def move_to_foundation(self, card):
        suit,value=card[0],int(card[1:])
        if suit=='H':
            if ((value==1 and not self.foundations[0]) or 
                    (self.foundations[0] and value==int(self.foundations[0][-1][1:])+1)):
                return 0
        elif suit=='D':
            if ((value==1 and not self.foundations[1]) or 
                    (self.foundations[1] and value==int(self.foundations[1][-1][1:])+1)):
                return 1
        elif suit=='S':
            if ((value==1 and not self.foundations[2]) or 
                    (self.foundations[2] and value==int(self.foundations[2][-1][1:])+1)):
                return 2
        elif suit=='C':
            if ((value==1 and not self.foundations[3]) or 
                    (self.foundations[3] and value==int(self.foundations[3][-1][1:])+1)):
                return 3

    def move_to_stack(self, card):
        yield from (idx for idx,stack in enumerate(self.stacks) if stack and 
                    self.move_to_stack_requirements(card,stack[-1]) or not stack)

    def move(self, card):

        foundation_idx, freecell_idx, stack_idx = self.move_to_foundation(card),\
                    self.move_to_freecell(card),[idx for idx in self.move_to_stack(card)]
        if foundation_idx in (range(4)):
            new_board = [Board.new_board(self.board), None]
            new_board[0].remove(card)
            new_board[0].foundations[foundation_idx].append(card)
            new_board[1] = 'foundation {}'.format(card)
            return [tuple(new_board)]

        if stack_idx:
            new_boards = [[Board.new_board(self.board), None]for j in range(len(stack_idx))]
            for idx,new_board in zip(stack_idx,new_boards):
                new_board[0].remove(card)
                new_board[0].stacks[idx].append(card)
                new_board[1] = 'newstack {}'.format(card) if not self.stacks[idx] else\
                         'stack {0} {1}'.format(card, self.stacks[idx][-1])
            return [tuple(new_board) for new_board in new_boards]
        
        if freecell_idx in range(4):
            new_board = [Board.new_board(self.board), None]
            new_board[0].remove(card)
            new_board[0].freecells[freecell_idx]=card
            new_board[1] = 'freecell {}'.format(card)
            return [tuple(new_board)]

        return [(Board.new_board(self.board),None)]

    def _children(self):
        if not all(not s for s in self.stacks):
            cards_to_move = tuple(list(list(zip(*[reversed(card) for card in self.stacks if card]))[0])+\
                            list([card for card in self.freecells if card]))
        else:
            cards_to_move = tuple([card for card in self.freecells if card])

        yield from [self.move(card) for card in cards_to_move]

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

def heuristic_function(board: Board):
    empty_freecells=board.freecells.count(0)
    cards_in_foundations=sum([len([sublist for sublist in each_foundation])\
                                 for each_foundation in board.foundations])
    empty_stacks=sum([not stack for stack in board.stacks])

    return cards_in_foundations*60+empty_stacks*30+empty_freecells*10

class PriorityQueue:
    class BoardPathPair:
        def __init__(self, board, path, score):
            self.board = board
            self.path = path
            self.value = score

        def __lt__(self, other):
            return self.value > other.value

    def __init__(self, heuristic):
        self.heap = []
        self.heuristic = heuristic
    
    def get(self):
        board_path = heapq.heappop(self.heap)
        return board_path.board, board_path.path

    def empty(self):
        return len(self.heap)==0

    def __len__(self):
        return len(self.heap)
    
class PQAstar(PriorityQueue):
    def __init__(self, heuristic):
        super().__init__(heuristic)

    def put(self, board_path: tuple):
        board, path = board_path
        heapq.heappush(self.heap, \
            PriorityQueue.BoardPathPair(board, path, self.heuristic(board)+len(path)))

class PQBestFirst(PriorityQueue):
    def __init__(self, heuristic):
        super().__init__(heuristic)

    def put(self, board_path: tuple):
        board, path = board_path
        heapq.heappush(self.heap, \
            PriorityQueue.BoardPathPair(board, path, self.heuristic(board)))

class BestFirst:
    def __init__(self, start_board, heuristic):
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

class AStar:
    def __init__(self, start_board, heuristic):
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
