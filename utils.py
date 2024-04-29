from collections import defaultdict
from typing import List

class Utlis:
    DIAMONDS = 0
    SPADES = 1
    CLUBS = 2
    HEARTS = 3

    FOUNDATION = "source"
    STACK = "stack"
    FREECELL = "freecell"
    NEWSTACK = "newstack"

    BREADTH = "breadth"
    DEPTH = "depth"
    BEST = "best"
    ASTAR = "astar"

    # Time limit up to 30 seconds
    LIMIT = 30000

    # N cards in a single foundation when game completed
    # gets updated when we initialize the initial state
    N = 0

    @staticmethod
    def get_method(method: str) -> str:
        method = method.lower()
        if method == MyUtils.BREADTH:
            return MyUtils.BREADTH
        elif method == MyUtils.DEPTH:
            return MyUtils.DEPTH
        elif method == MyUtils.BEST:
            return MyUtils.BEST
        else:
            print("Invalid method provided. Using ASTAR (because it's faster).")
            return MyUtils.ASTAR

    @staticmethod
    def get_foundation(state, value: str):
        return state.get_foundations().get(getattr(MyUtils, value))

    @staticmethod
    def get_card_by_identifier(state, suit: str, value: int):
        c = Card(suit, value)

        if c in state.get_freecells():
            return c

        for i in range(4):
            if state.get_foundations()[i] and state.get_foundations()[i][-1] == c:
                return c

        for i in range(8):
            if state.get_stacks()[i] and state.get_stacks()[i][-1] == c:
                return c

        return None

    @staticmethod
    def get_stack_idx_from_card(state, card):
        for i in range(8):
            if state.get_stacks()[i] and state.get_stacks()[i][-1] == card:
                return i
        return -1

    @staticmethod
    def get_foundation_idx_from_card(state, card):
        for i in range(8):
            if state.get_foundations()[i] and state.get_foundations()[i][-1] == card:
                return i
        return -1
