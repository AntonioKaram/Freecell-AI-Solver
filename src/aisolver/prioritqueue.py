import heapq

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
            PriorityQueue.BoardPathPair(board, path, -self.heuristic(board)-len(path)))

class PQBestFirst(PriorityQueue):
    def __init__(self, heuristic):
        super().__init__(heuristic)

    def put(self, board_path: tuple):
        board, path = board_path
        heapq.heappush(self.heap, \
            PriorityQueue.BoardPathPair(board, path, -self.heuristic(board)))
