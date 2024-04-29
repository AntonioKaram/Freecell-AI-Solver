"""
    Defines a card object for the freecell solver
"""

class Card:
    def __init__(self, value):
        self.encoding = self.encode_card(value)
        self.value = int(self.encoding[1])
        self.suit = self.encoding[0]
        self.color = "black" if self.suit in ('S', 'C') else "red"
    
    # Overload hash function for data strucutre storing
    def __hash__(self):
        return hash((self.color, self.suit, self.value))

    # Overloading equality check
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.color == other.color and self.suit == other.suit and self.value == other.value
        return False

    # Overloading string defenition
    def __str__(self):
        return f"{self.suit}{self.value}"

    # Define comparison operations
    def is_smaller_and_different_color(self, card):
        return (self.value + 1) == card.value and self.color.lower() != card.color.lower()

    def is_larger_and_same_suit(self, card):
        return (self.value - 1) == card.value and self.suit == card.suit
    
    # Decode hex value from memory file
    def encode_card(self,card_code):
    
        # Define the mapping of card codes to suit letters
        suit_mapping = {
            0: 'C',
            1: 'D',
            2: 'S',
            3: 'H'
        }

        # Extract the rank and suit from the card code
        rank = card_code // 4
        suit = card_code % 4

        # Convert rank to a letter (A, 2, 3, ..., K)
        rank_letter = str(rank + 1) if rank < 9 else ['T', 'J', 'Q', 'K'][rank - 9]

        # Construct the final representation
        card = f"{suit_mapping[suit]}{rank_letter}"

        return card

    # Define cloning
    def clone(self):
        return Card(self.suit, self.value)

    # Create setters and getters
    def get_suit(self):
        return self.suit

    def set_suit(self, suit):
        self.suit = suit

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

# Example usage
if __name__ == "__main__":
    card1 = Card(0x0D) # 4 of diamonds
    card2 = Card(0x18) # 7 of clubs
    
    print(card1.is_smaller_and_different_color(card2))
    print(card1 == card2)
