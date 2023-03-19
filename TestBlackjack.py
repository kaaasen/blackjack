import unittest
from blackjack import *

class TestBlackjack(unittest.TestCase):
    
    def test_new_deck(self):
        """Test that a new deck is created with the correct number of cards."""
        deck = new_deck()
        self.assertIsInstance(deck, dict)
        self.assertEqual(len(deck), 52)

    def test_deal_initial_cards_values(self):
        """Test that the first/second cards dealt to the player and Marit have values within what we expect."""
        new_deck()
        deal_initial_cards("player")
        deal_initial_cards("marit")
        player_card = int(player_cards[0]["value"])
        marit_card = int(marit_cards[1]["value"])
        self.assertIn(player_card, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertIn(marit_card, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        
    def test_create_cards_string(self):
        """Test that a string representation of the cards is correctly created."""
        cards = [
            {"value": "A", "original_value": "A", "suit": "hearts"},
            {"value": "10", "original_value": "10", "suit": "spades"},
            {"value": "K", "original_value": "K", "suit": "diamonds"}
        ]
        cards_string = create_cards_string(cards)
        self.assertEqual(cards_string, "HA, S10, DK")
        
if __name__ == '__main__':
    unittest.main()
