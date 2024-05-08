class Card:
        
    # Convert from hex value to card code
    def encode_card(card_code):
    
        # Conversion dictionary
        suit_mapping = {
            0: 'C',
            1: 'D',
            2: 'H',
            3: 'S'
        }

        # Conversion logic
        rank = card_code // 4
        suit = card_code % 4
        rank_letter = str(rank + 1) if rank < 9 else ['10', '11', '12', '13'][rank - 9]

        # Get card code
        return f"{suit_mapping[suit]}{rank_letter}"


    # Convert from card code to path of image
    def card_code_to_pic(card_code):
        
        # Need 0 padding for the filename
        pad_zeros = lambda x: str(x) if len(str(x))>=2 else '0'*(2-len(str(x)))+str(x)
        
        # Conversion dictionaries
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
        
        # Conversion logic
        suit = card_code[0]
        rank_start = suit_char_to_num[suit]*13
        card_num = pad_zeros(rank_start + int(card_code[1:]))
        
        # Get filename
        return f"../data/img/cards_{card_num}_{suit_num_to_name[suit_char_to_num[suit]]}.bmp"

    # Convert from card code to card name
    def code_to_name(code):
        
        #Conversion dictionary
        suit_to_str = {
            'C': ' of Clubs',
            'D': ' of Diamonds',
            'H': ' of Hearts',
            'S': ' of Spades',
        }

        # Conversion logic
        suit = suit_to_str[code[0]]
        value = code[1:] if int(code[1:]) < 11 else ['Jack', 'Queen', 'King'][int(code[1:])%11]
        value = value if value != "1" else "Ace"

        # Get card name
        return str(value) + suit


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

    
    
