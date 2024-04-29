import sys
from card import Card
from state import State
from frontier import Frontier
import processMemoryReader as pmr

# Globals
method = ""
game_deck = []
num_columns = 8
card_byte_offset = 4
card_enumeration = {}
column_byte_offset = 54
process_name = "Freecell.exe"
column_base_address = 0x01007554
stack_length = [7, 7, 7, 7, 6, 6, 6, 6]

def main():
    
    # Initialize memory reader for the running process
    memory_reader = pmr.processMemoryReader(process_name=process_name)
    
    # Initialize solver state
    initial_state = State()
    
    # Iterate through memory chunk of each column
    for i in range(num_columns):
        column_cards = []

        # Calculate the chunk's address
        column_address = column_base_address + (i * column_byte_offset)
        
        # Iterate through the cards in the chunk
        for j in range(stack_length[i]):
        
            # Read the cards in the chunk
            card_hex = memory_reader.read_memory(column_address + (j*card_byte_offset)) 
            
            # Add card to initial state
            card = Card(card_hex)
            initial_state.columns[i].append(card)
            initial_state.pair[card] = 'STACK'
            
    
    # Initialize frontier
    frontier = Frontier()
    
    # Start search
    frontier.search(initial_state, method, "data.text")


if __name__=="__main__":
    main()