import copy

class Board:
    
    # Constant highest card
    MAX_CARD = 13

    def __init__(self, board):
        
        # Board has stacks, freecells, and foundations
        self.board = tuple(board)
        self.stacks = board[0]
        self.freecells = board[1]
        self.foundations = board[2]

    # Override string declaration
    def __str__(self):
        return '{}'.format(self.board)

    # Override key directive
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
    
    # Get card location
    def card_index(self, card):
        if card in self.freecells:
            return ('freecells', self.freecells.index(card))
        else:
            return ('stacks', next((i for i,stack in enumerate(self.stacks) if card in stack),None))

    # Remove a card
    def remove(self, card):
        (place, idx) = self.card_index(card)
        if place=='freecells':
            self.freecells[idx]=0
        else:
            self.stacks[idx].pop()

    # Rules for moving to the stack
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
    
    # Rules for reaching the goal
    def goal(self):
        done = 0
        for idx,suit in zip(range(4),('H','D','S','C')):
            if self.foundations[idx] and self.foundations[idx][-1]==suit+str(self.MAX_CARD):
                done+=1
        return True if done==4 else False

    # Get index for moving to freecell
    def move_to_freecell(self):
        return next((idx for idx,val in enumerate(self.freecells) if not val),None)

    # Get index for moving to foundation
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

    # Get index for moving to stack
    def move_to_stack(self, card):
        yield from (idx for idx,stack in enumerate(self.stacks) if stack and 
                    self.move_to_stack_requirements(card,stack[-1]) or not stack)

    # Move the card
    def move(self, card):

        foundation_idx = self.move_to_foundation(card)
        freecell_idx = self.move_to_freecell()
        stack_idx = [idx for idx in self.move_to_stack(card)]
        
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

    # Get a generator of children
    def _children(self):
        if not all(not s for s in self.stacks):
            cards_to_move = tuple(list(list(zip(*[reversed(card) for card in self.stacks if card]))[0])+\
                            list([card for card in self.freecells if card]))
        else:
            cards_to_move = tuple([card for card in self.freecells if card])

        yield from [self.move(card) for card in cards_to_move]
