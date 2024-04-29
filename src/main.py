import sys
import time
from card import Card
from solver import Board, BFS, DFS, AStar, BestFirst, heuristic_function
import processMemoryReader as pmr



# Globals
method = "best"
outfile = "out.txt"
game_deck = []
num_columns = 8
card_byte_offset = 4
card_enumeration = {}
column_byte_offset = 54
process_name = "Freecell.exe"
column_base_address = 0x01007554
stack_length = [7, 7, 7, 7, 6, 6, 6, 6]

def write_to_file(path: list, filename: str):
        with open(filename, 'w') as outfile:
            try:
                outfile.write(str(len(path))+'\n')
                outfile.write('\n'.join(move for move in path))
                print('Solution written to file {}'.format(filename))
            except IOError as e:
                raise e

def main():
    
    # Initialize memory reader for the running process
    memory_reader = pmr.processMemoryReader(process_name=process_name)
        
    # Iterate through memory chunk of each column
    for i in range(num_columns):
        column_cards = []

        # Calculate the chunk's address
        column_address = column_base_address + (i * column_byte_offset)
        
        # Iterate through the cards in the chunk
        for j in range(stack_length[i]):
        
            # Read the cards in the chunk
            card_hex = memory_reader.read_memory(column_address + (j*card_byte_offset)) 
            
            # Add card to column
            card = Card.encode_card(card_hex)
            column_cards.append(card)
            
        # Add column to deck   
        game_deck.append(column_cards)
    
    # Initialize game
    start_freecells = 4*[0]
    start_foundations = [[] for j in range(4)]
    
    # Initialize board
    start_board = Board((game_deck, start_freecells, start_foundations))
            
    start = time.time()    
    
    if method=='breadth':
        seeker = BFS(start_board)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = 0
        
        if path:
            write_to_file(path, outfile)
        else:
            print('No solution found')

    elif method=='depth':
        seeker = DFS(start_board)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = 0
        
        if path:
            write_to_file(path, outfile)
        else:
            print('No solution found')

    elif method=='astar':
        seeker = AStar(start_board, heuristic_function)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = 0
        
        if path:
            write_to_file(path, outfile)
        else:
            print('No solution found')
    
    elif method=='best':
        seeker = BestFirst(start_board, heuristic_function)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = 0
        
        if path:
            write_to_file(path, outfile)
        else:
            print('No solution found')
    else:
        print('Enter a valid method {breadth, depth, astar, best}')
        sys.exit(1)

    print('Time taken: {}s'.format(str(time.time()-start)[:5]))


if __name__=="__main__":
    main()