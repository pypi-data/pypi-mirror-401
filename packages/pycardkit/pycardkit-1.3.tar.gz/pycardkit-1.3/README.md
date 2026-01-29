# CardKit

A Python library for cards and decks with context-dependent rules, supporting various card games like Poker, Blackjack, Baccarat, and more.

## Features

- **Flexible Card Representation**: Cards with ranks, suits, and game-specific values.
- **Context-Dependent Rules**: Easily switch between different card game rules using predefined contexts.
- **Deck Management**: Shuffle, draw cards from top or bottom, reset, and compare cards.
- **Game-Specific Contexts**: Predefined rank values for Poker, Blackjack, Baccarat, Rummy, Bridge, War, and Crazy Eights.

## Installation

Install CardKit via pip:

```bash
pip install pycardkit
```

## Usage

### Basic Usage

Import the necessary classes and contexts:

```python
from pycardkit import Card, Deck, card_context
```

### Creating Cards

Create a card with a specific context:

```python
# Using Poker context
card = Card("A", "Hearts", card_context.POKER_RANK_VALUES)
print(card)  # Output: A of Hearts
print(card.value)  # Output: 14
```

### Creating and Managing Decks

Create a deck with a context:

```python
deck = Deck(card_context.BLACKJACK_RANK_VALUES)
deck.shuffle()

# Draw cards
hand = deck.grab_cards_top(5)
for card in hand:
    print(card)
```

### Comparing Cards

Compare two cards based on the deck's rules:

```python
card1 = Card("K", "Spades", card_context.POKER_RANK_VALUES)
card2 = Card("Q", "Hearts", card_context.POKER_RANK_VALUES)
diff = deck.compare(card1, card2)
if diff > 0:
    print("Card1 is higher")
elif diff < 0:
    print("Card2 is higher")
else:
    print("Cards are equal")
```

### Ordering Hands

Order a hand of cards:

```python
hand = [Card("5", "Clubs", card_context.POKER_RANK_VALUES),
        Card("A", "Hearts", card_context.POKER_RANK_VALUES),
        Card("K", "Diamonds", card_context.POKER_RANK_VALUES)]
ordered_hand = deck.order_cards(hand)
for card in ordered_hand:
    print(card)
```

### Card Properties

Check various properties of a card:

```python
card = Card("K", "Hearts", card_context.POKER_RANK_VALUES)
print(f"Is face card: {card.is_face()}")  # Output: True
print(f"Is ace: {card.is_ace()}")        # Output: False
print(f"Color: {card.get_color()}")      # Output: Red
```

### Direct Card Comparisons

Use comparison operators for cards:

```python
card1 = Card("A", "Spades", card_context.POKER_RANK_VALUES)
card2 = Card("K", "Hearts", card_context.POKER_RANK_VALUES)
print(card1 > card2)  # Output: True (Ace is higher in Poker)
print(card1 == card2) # Output: False
```

### Drawing from Bottom and Resetting

Draw cards from the bottom and reset the deck:

```python
deck = Deck(card_context.BLACKJACK_RANK_VALUES)
deck.shuffle()
bottom_cards = deck.grab_cards_bottom(3)
print("Bottom cards:")
for card in bottom_cards:
    print(card)

deck.reset()  # Reset to ordered deck
print(f"Deck size after reset: {len(deck.deck)}")
```

## Game-Specific Examples

### Poker

```python
from pypycardkit import Deck, card_context

deck = Deck(card_context.POKER_RANK_VALUES)
deck.shuffle()
hand = deck.grab_cards_top(5)
print("Poker Hand:")
for card in hand:
    print(f"{card} - Value: {card.value}")
```

### Blackjack

```python
from pycardkit import Deck, card_context

deck = Deck(card_context.BLACKJACK_RANK_VALUES)
deck.shuffle()
player_hand = deck.grab_cards_top(2)
dealer_hand = deck.grab_cards_top(2)

print("Player Hand:")
for card in player_hand:
    print(f"{card} - Value: {card.value}")

print("Dealer Hand:")
for card in dealer_hand:
    print(f"{card} - Value: {card.value}")
```

### Baccarat

```python
from pycardkit import Deck, card_context

deck = Deck(card_context.BACCARAT_RANK_VALUES)
deck.shuffle()
player_card = deck.grab_cards_top(1)[0]
banker_card = deck.grab_cards_top(1)[0]

print(f"Player Card: {player_card} - Value: {player_card.value}")
print(f"Banker Card: {banker_card} - Value: {banker_card.value}")
```

## API Reference

### Card Class

- `__init__(rank: str, suit: str, context: dict)`: Initialize a card. Raises ValueError for invalid rank or suit.
- `__str__()`: String representation.
- `__repr__()`: Representation for debugging.
- `__eq__(other)`: Check equality based on rank and suit.
- `__gt__(other)`: Greater than comparison using deck rules.
- `__lt__(other)`: Less than comparison using deck rules.
- `is_face() -> bool`: Check if the card is a face card (J, Q, K).
- `is_ace() -> bool`: Check if the card is an Ace.
- `get_color() -> str`: Get the color of the card ('Red' or 'Black').

### Deck Class

- `__init__(context: dict)`: Initialize a deck with a context.
- `shuffle()`: Shuffle the deck.
- `grab_cards_top(amount)`: Draw cards from the top.
- `grab_cards_bottom(amount)`: Draw cards from the bottom.
- `reset()`: Reset the deck to ordered state.
- `compare(card1, card2)`: Compare two cards.
- `order_cards(hand)`: Order a list of cards.

### Contexts

Available contexts in `pycardkit.card_context`:

- `POKER_RANK_VALUES`
- `POKER_ACE_LOW_RANK_VALUES`
- `POKER_ACE_FLEXIBLE_RANK_VALUES`
- `BLACKJACK_RANK_VALUES`
- `BACCARAT_RANK_VALUES`
- `RUMMY_RANK_VALUES`
- `RUMMY_ACE_HIGH_RANK_VALUES`
- `BRIDGE_RANK_VALUES`
- `WAR_RANK_VALUES`
- `CRAZY_EIGHTS_RANK_VALUES`

## License

This project is licensed under the MIT License.