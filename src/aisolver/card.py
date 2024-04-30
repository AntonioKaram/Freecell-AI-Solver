import sys
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image

class Card:
    # Decode hex value from memory file
    def encode_card(card_code):
    
        # Define the mapping of card codes to suit letters
        suit_mapping = {
            0: 'C',
            1: 'D',
            2: 'H',
            3: 'S'
        }

        # Extract the rank and suit from the card code
        rank = card_code // 4
        suit = card_code % 4

        # Convert rank to a letter (A, 2, 3, ..., K)
        rank_letter = str(rank + 1) if rank < 9 else ['10', '11', '12', '13'][rank - 9]

        # Construct the final representation
        card = f"{suit_mapping[suit]}{rank_letter}"

        return card

pad_zeros = lambda x: str(x) if len(str(x))>=2 else '0'*(2-len(str(x)))+str(x)

# C1, D13, H2, S5
def card_code_to_pic(card_code):
    suit_char_to_num = {
            'C': 0,
            'D': 1,
            'H': 2,
            'S': 3,
        }
    suit_num_to_name = {
            0: 'clubs',
            1: 'diamonds',
            2: 'hearts',
            3: 'spades'
        }
    suit = card_code[0]
    rank_start = suit_char_to_num[suit]*13
    card_num = pad_zeros(rank_start + int(card_code[1:]))
    file_name = f"../data/img/cards_{card_num}_{suit_num_to_name[suit_char_to_num[suit]]}.bmp"
    return file_name

def code_to_name(code):
    suit_to_str = {
        'C': ' of Clubs',
        'D': ' of Diamonds',
        'H': ' of Hearts',
        'S': ' of Spades',
    }


    suit = suit_to_str[code[0]]
    value = code[1:] if int(code[1:]) < 11 else ['Jack', 'Queen', 'King'][int(code[1:])%11]
    value = value if value != "1" else "Ace"

    return str(value) + suit


def addQtImage(path, window, layout):
    label = QLabel(window)
    pixmap = QPixmap(path)
    label.setPixmap(pixmap)
    # window.resize(1000, 1000) 
    layout.addWidget(label)

# Example usage
if __name__ == "__main__":
    card1 = Card.encode_card(0x0D) # 4 of diamonds
    card2 = Card.encode_card(0x18) # 7 of clubs
    card3 = Card.encode_card(0x00) # Ace of clubs
    card4 = Card.encode_card(0x01) # Ace of diamonds
    card5 = Card.encode_card(0x02) # Ace of spades
    
    print(card1)
    print(card2)
    print(card3)
    print(card4)
    print(card5)

    class Menu(QMainWindow):

        def __init__(self):
            super().__init__()
            self.setWindowTitle("Title")
            
            self.central_widget = QWidget()               
            self.setCentralWidget(self.central_widget)    
            lay = QVBoxLayout(self.central_widget)

            label = QLabel(self)
            pixmap = QPixmap('cards_01_clubs.bmp')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            
            lay.addWidget(label)
            # addQtImage(card_code_to_pic('C1'), self, lay)
            self.show()

    # for i in ['C1', 'D13', 'H2', 'S5']:
    #     print(card_code_to_pic(i))

    app = QApplication(sys.argv)
    ex = Menu()
    app.exec_()
    sys.exit()
    
    
