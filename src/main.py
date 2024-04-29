import sys
from aisolver.card import Card
from aisolver.board import Board
from gui import QApplication, MainWindow
import memory.processMemoryReader as pmr

# Globals
game_deck = []
num_columns = 8
method = "best"
outfile = "out.txt"
card_byte_offset = 4
card_enumeration = {}
column_byte_offset = 54
process_name = "Freecell.exe"
column_base_address = 0x01007554
stack_length = [7, 7, 7, 7, 6, 6, 6, 6]
    
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
    
    # Start GUI
    app = QApplication(sys.argv)
    
    # Show window
    window = MainWindow(start_board)
    window.show()
    
    # Launch GUI
    app.exec_()
        

    
    


if __name__=="__main__":
    main()