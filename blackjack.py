try:
    import requests
except ImportError:
    print("Please install the requests module to run this code.")
    exit()
    
# global variables because of lazyness / lack of time
global player_cards
global marit_cards
global marit_score
marit_score = 0
player_cards = [] 
marit_cards = []

def deal_initial_cards(user_id):
    # Deal the first two cards to the user.
    for key in list(deck.keys())[:2]:
        # Add the original value to the card for later use if it's an Ace.
        deck[key]["original_value"] = deck[key]["value"]
        # If the card is a King, Queen, or Jack, set its value to 10.
        if deck[key]["value"] in ["K", "Q", "J"]:
            deck[key]["value"] = 10
        # If the card is an Ace, set its value to 11.
        if deck[key]["value"] == "A":
            deck[key]["value"] = 11

        # Add the card to the user's hand.
        new_card = deck[key]
        if user_id == "player":
            player_cards.append(new_card)
        elif user_id == "marit":
            marit_cards.append(new_card)
        
        # Remove the card from the deck.
        deck.pop(key)
        
def draw_card(user_id):
    # Select the top card from the deck.  
    for key in list(deck.keys())[:1]:
        # Add the original value of the card to the card's dictionary entry in the deck.
        deck[key]["original_value"] = deck[key]["value"]  
        
        # If the card's value is A, K, Q, or J, change its value to 10.
        if deck[key]["value"] in ["A", "K", "Q", "J"]: 
            deck[key]["value"] = 10

        # Store the card in a new_card variable.
        new_card = deck[key] 
        
        # If the user is the player, add the card to the player's hand.
        if user_id == "player":
            #print(f"player drew and additional card ", new_card)
            player_cards.append(new_card)
            
        # If the user is Marit, add the card to Marit's hand, and return the card.
        elif user_id == "marit":
            #print(f"marit drew an additional card ", new_card)
            marit_cards.append(new_card)
            return new_card
            
        # Remove the card from the deck.
        deck.pop(key)
          
def new_deck():
    """Create a new deck and return its ID."""
    url = "https://blackjack.labs.nais.io/shuffle"
    try:
        response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        exit()
        
    global deck
    deck = {}
    for index, value in enumerate(response):
        deck[index] = value
    
    return deck

def calculate_score(cards):
    """Take a list of cards and return the score calculated from the cards."""
    # Check if the sum of the cards is 21 and if there are exactly two cards, which represents a blackjack.
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    # Check if there is an Ace (11) in the list of cards and if the sum of the cards is greater than 21, which represents a bust.
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)  # remove one of the Aces from the cards
        cards.append(1)   # add an Ace with a value of 1 to the cards
    # Return the sum of the cards.
    return sum(cards)
        
def create_cards_string(cards):
    cards_string = ""  # Initialize an empty string to store the card strings.
    card_set = set()  # Initialize a set to keep track of which cards have already been added to the string.
    
    for card in cards:  # Iterate over the list of cards.
        if card is None:  # If the card is None, remove it from the list and skip to the next card.
            cards.remove(card)
            continue
        
        suit = card["suit"]  # Get the suit of the card from the card dictionary.
        value = card["original_value"]  # Get the value of the card from the card dictionary.
        
        # Convert the suit to a single-character abbreviation.
        if suit.lower() == "hearts":
            suit = "H"
        elif suit.lower() == "spades":
            suit = "S"
        elif suit.lower() == "diamonds":
            suit = "D"
        elif suit.lower() == "clubs":
            suit = "C"
        
        card_string = suit + str(value)  # Concatenate the suit abbreviation and value to create a string representation of the card.
        
        if card_string in card_set:  # If the card has already been added to the string, skip it.
            continue
        
        card_set.add(card_string)  # Add the card string to the set of already-added cards.
        cards_string += card_string + ", "  # Add the card string to the overall string representation of the cards.
    
    cards_string = cards_string.rstrip(", ")  # Remove the trailing comma and space from the string.
    return cards_string  # Return the final string representation of the cards.

def play_game():
    """Play a game of Blackjack."""
    deck = new_deck()
    is_game_over = False

    # Deal initial cards to both the player and Marit
    player_cards.append(deal_initial_cards("player"))
    marit_cards.append(deal_initial_cards("marit"))

    # Keep playing until the game is over
    while not is_game_over:
        # Initialize scores and index for both players' cards
        player_score = 0
        marit_score = 0
        player_index = 0
        marit_index = 0

        # Iterate through each player's cards and calculate their score
        while player_index < len(player_cards):
            if player_cards[player_index] is None:
                player_cards.pop(player_index)
                continue
            card_value = int(player_cards[player_index]["value"])
            player_score += card_value
            player_index += 1

        while marit_index < len(marit_cards):
            if marit_cards[marit_index] is None:
                marit_cards.pop(marit_index)
                continue
            card_value = int(marit_cards[marit_index]["value"])
            marit_score += card_value
            marit_index += 1

        # Check if the player has stopped drawing or has a score above 17
        if player_score == 0 or marit_score == 0 or player_score >= 17:
            is_game_over = True
        # If not, draw another card for the player
        else:
            player_cards.append(draw_card("player"))

    # Marit starts drawing if the player has stopped drawing or has a score above 17
    while 0 < marit_score < 17:
        # print("Marit should draw a card! Her current score is ", marit_score)
        if marit_score >= 17:
            is_game_over = True
        elif player_score > 21:
            is_game_over = True
            break
        else:
            drawn_card = draw_card("marit")
            marit_cards.append(drawn_card)
            # print(f"marit_score: ", marit_score, " new card has value ", drawn_card["value"], ". Total score should be ", marit_score + int(drawn_card["value"]))
            drawn_card_value = int(drawn_card["value"])
            marit_score += drawn_card_value
            # print(f"after adding the new card to marit's score, her score is now: ", marit_score)
            continue
        
    if player_score > 21:
        print("Marit won!")
    elif marit_score > 21:
        print("Player won!")
    elif player_score > marit_score:
        print("Player won!")
    elif marit_score > player_score:
        print("Marit won!")
    else:
        print("It's a tie!")

    # print the final hands of both players
    player_cards_string = create_cards_string(player_cards)
    marit_cards_string = create_cards_string(marit_cards)

    print(f"Player | {player_score} | {player_cards_string}")
    print(f"Marit | {marit_score} | {marit_cards_string}")

play_game()