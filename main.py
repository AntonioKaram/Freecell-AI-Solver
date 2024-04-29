import sys
import processMemoryReader as pmr

# Globals
game_deck = []
num_columns = 8
card_byte_offset = 4
column_byte_offset = 54
process_name = "Freecell.exe"
column_base_address = 0x01007554
stack_length = [7, 7, 7, 7, 6, 6, 6, 6]
card_enumeration = {}

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
            value = memory_reader.read_memory(column_address + (j*card_byte_offset))            
            column_cards.append(value)
        
        # Add read cards into game deck
        game_deck.append(column_cards)
        
        
    # Initialize solver state
    
    
        



if __name__=="__main__":
    main()