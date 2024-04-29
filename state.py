class State:
    def __init__(self):
        self.freecells = []
        self.foundations = [[] for _ in range(4)]
        self.stacks = [[] for _ in range(8)]
        self.pair = {}
        self.move = ""
        self.method = ""
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def print_state(self):
        print("-------- State -----------")
        print("freecells:", self.freecells)
        print()
        print("foundation:")
        for stack in self.foundations:
            print(stack)
        print()
        print("stacks:")
        for stack in self.stacks:
            print(stack)
        print("-------- End State ---------")

    def __hash__(self):
        return hash((tuple(self.foundations), tuple(self.freecells), self.method, tuple(self.stacks)))

    def __eq__(self, other):
        if not other:
            return False
        if self is other:
            return True
        if len(self.freecells) != len(other.freecells):
            return False
        for card in self.freecells:
            if card not in other.freecells:
                return False
        for i in range(4):
            if len(self.foundations[i]) != len(other.foundations[i]):
                return False
            for c in self.foundations[i]:
                if c not in other.foundations[i]:
                    return False
        for i in range(8):
            if len(self.stacks[i]) != len(other.stacks[i]):
                return False
            if self.stacks[i] and other.stacks[i] and self.stacks[i][-1] != other.stacks[i][-1]:
                return False
        return True

    def __lt__(self, other):
        if self == other:
            return 0
        if self.method == "BREADTH":
            return 1 if self.g > other.g else -1
        elif self.method == "DEPTH":
            return -1 if self.g > other.g else 1
        elif self.method == "BEST":
            if self.h > other.h:
                return 1
            elif self.h < other.h:
                return -1
            else:
                return -1 if self.g < other.g else 1
        else:
            if self.f > other.f:
                return 1
            elif self.f < other.f:
                return -1
            else:
                return -1 if self.g < other.g else 1

    def clone(self):
        state = State()
        state.method = self.method
        for c in self.freecells:
            state.freecells.append(c.clone())
            state.pair[c] = "FREECELL"
        for i in range(4):
            for c in self.foundations[i]:
                state.foundations[i].append(c.clone())
                state.pair[c] = "FOUNDATION"
        for i in range(8):
            for c in self.stacks[i]:
                state.stacks[i].append(c.clone())
                state.pair[c] = "STACK"
        return state

    def move_card_to_freecell(self, card):
        self.remove_card_from_its_position(card)
        self.freecells.append(card)
        self.pair[card] = "FREECELL"

    def move_card_to_stack(self, card_to_move, stack):
        self.remove_card_from_its_position(card_to_move)
        stack.append(card_to_move)
        self.pair[card_to_move] = "STACK"

    def remove_card_from_its_position(self, card):
        for i in range(4):
            if card in self.foundations[i]:
                self.foundations[i].remove(card)
        for i in range(8):
            if card in self.stacks[i]:
                self.stacks[i].remove(card)
    def move_card_to_foundation(self, card_to_move, foundation):
        self.remove_card_from_its_position(card_to_move)
        foundation.append(card_to_move)
        self.pair[card_to_move] = "FOUNDATION"
        return True

    def freecell_rule(self, card):
        return len(self.freecells) < 4

    def foundation_rule(self, card_to_move, foundation):
        if not foundation and card_to_move.value == 0:
            return True
        if foundation and card_to_move.is_larger_and_same_suit(foundation[-1]):
            return True
        return False

    def stack_rule(self, card_to_move, stack):
        if not stack:
            return True
        if card_to_move.is_smaller_and_different_color(stack[-1]):
            return True
        return False

    def is_solved(self):
        if self.freecells:
            return False
        for stack in self.stacks:
            if stack:
                return False
        for foundation in self.foundations:
            prev_card = None
            for card in foundation:
                if prev_card:
                    if prev_card.suit != card.suit or prev_card.value >= card.value:
                        return False
                prev_card = card
        return True

    def remove_card_from_its_position(self, card_to_move):
        if self.pair[card_to_move] == "FREECELL":
            self.freecells.remove(card_to_move)
        elif self.pair[card_to_move] == "STACK":
            for stack in self.stacks:
                if stack and stack[-1] == card_to_move:
                    stack.pop()
                    break
        elif self.pair[card_to_move] == "FOUNDATION":
            foundation = self.get_foundation(card_to_move.suit)
            foundation.remove(card_to_move)

    def get_children_of_state(self, method):
        children = []
        children.extend(self.get_moves_from_foundation_to_other_position(method))
        children.extend(self.get_moves_from_stack_to_other_position(method))
        children.extend(self.get_moves_from_freecells_to_other_position(method))
        return children

    def get_moves_from_freecells_to_other_position(self, method):
        children = []
        if not self.freecells:
            return children
        for card in self.freecells:
            card_to_move = card.clone()
            has_moved_to_new_stack = False
            children_state = self.expanded_to_foundation(card_to_move, self.get_foundation(card_to_move.suit))
            if children_state:
                children.append(children_state)
            for i in range(8):
                if self.stack_rule(card_to_move, self.stacks[i]):
                    if self.stacks[i] and has_moved_to_new_stack:
                        continue
                    children_state = self.clone()
                    children_state.move_card_to_stack(card_to_move, children_state.stacks[i])
                    children_state.set_parent(self)
                    children_state.set_h(children_state.heuristic_function())
                    children_state.set_f(method, children_state)
                    if not self.stacks[i]:
                        children_state.set_move(f"NEWSTACK {card_to_move}")
                        has_moved_to_new_stack = True
                    else:
                        children_state.set_move(f"STACK {card_to_move} {self.stacks[i][-1]}")
                    children.append(children_state)
        return children
    
    def get_moves_from_stack_to_other_position(self, method):
        children = []
        for i in range(8):
            if self.stacks[i].empty():
                continue
            card_to_move = self.stacks[i][-1].clone()
            has_moved_to_new_stack = False
            children_state = self.expanded_to_foundation(card_to_move, self.get_foundation(card_to_move.suit))
            if children_state:
                children.append(children_state)
            children_state = None
            for j in range(8):
                if i == j:
                    continue
                if self.stacks[i].size() == 1 and self.stacks[j].empty():
                    continue
                if self.stack_rule(card_to_move, self.stacks[j]):
                    if self.stacks[j].empty() and has_moved_to_new_stack:
                        continue
                    children_state = self.clone()
                    children_state.move_card_to_stack(card_to_move, children_state.stacks[j])
                    children_state.set_parent(self)
                    children_state.set_h(children_state.heuristic_function())
                    children_state.set_f(method, children_state)
                    if self.stacks[j].empty():
                        children_state.set_move(f"{MyUtils.NEWSTACK} {card_to_move}")
                        has_moved_to_new_stack = True
                    else:
                        children_state.set_move(f"{MyUtils.STACK} {card_to_move} {self.stacks[j][-1]}")
                    children.append(children_state)
                    children_state = None
            children_state = self.expanded_to_freecell(card_to_move)
            if children_state:
                children.append(children_state)
        return children

    def expanded_to_foundation(self, card_to_move, foundation):
        if self.foundation_rule(card_to_move, foundation):
            children_state = self.clone()
            children_state.move_card_to_foundation(card_to_move, self.get_foundation(card_to_move.suit))
            children_state.set_parent(self)
            children_state.set_h(children_state.heuristic_function())
            children_state.set_f(self.method, children_state)
            children_state.set_move(f"{MyUtils.FOUNDATION} {card_to_move}")
            return children_state
        return None
    
    
    
    