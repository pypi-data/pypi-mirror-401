from .card import Card
import random

class Deck():
    """
    Default class for decks.
    """
    def __init__(self, context: dict):
        self.ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.suit_order = ["Clubs","Diamonds","Hearts","Spades"]
        self.context = context
        self.reset()

    def shuffle(self):
        """
        Shuffles the deck.
        """
        random.shuffle(self.deck)

    def grab_cards_top(self, amount):
        """
        Grab 'amount' cards from the top of the deck.
        """
        remaining = 0
        if amount > len(self.deck):
            remaining = amount - len(self.deck)
            amount = len(self.deck)

        grabbed = [self.deck.pop(-1) for _ in range(amount)]

        if remaining > 0:
            self.shuffle()
            grabbed.extend([self.deck.pop(-1) for _ in range(remaining)])

        return grabbed
    
    def grab_cards_bottom(self, amount):
        """
        Grab 'amount' cards from the bottom of the deck.
        """
        remaining = 0
        if amount > len(self.deck):
            remaining = amount - len(self.deck)
            amount = len(self.deck)

        grabbed = [self.deck.pop(0) for _ in range(amount)]

        if remaining > 0:
            self.shuffle()
            grabbed.extend([self.deck.pop(0) for _ in range(remaining)])

        return grabbed
    
    def reset(self):
        """
        Orders and resets the deck.
        """
        self.deck = [Card(rank,suit,self.context) for rank in self.ranks for suit in self.suits]

    def compare(self, card1: Card, card2: Card):
        """
        Returns the value difference between card1 and card2.
        If the result is positive, it means card1 is better than card2.
        The opposite for negatives.
        0 means they are the same.

        :param card1: First card
        :type card1: Card
        :param card2: Second card
        :type card2: Card
        """
        v1 = card1.value
        v2 = card2.value

        if isinstance(v1, tuple):
            v1 = max(v1)
        if isinstance(v2, tuple):
            v2 = max(v2)

        diff = v1 - v2
        if diff == 0:
            diff = self.suit_order.index(card1.suit) - self.suit_order.index(card2.suit)

        return diff

    def order_cards(self, hand: list):
        """
        Orders the cards on a hand.
        """
        return sorted(
            hand,
            key=lambda card: (
                self.suit_order.index(card.suit),
                max(card.value) if isinstance(card.value, tuple) else card.value
            )
        )