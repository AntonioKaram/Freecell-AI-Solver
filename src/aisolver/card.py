class Card:
    # Decode hex value from memory file
    def encode_card(card_code):
    
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
    
    
