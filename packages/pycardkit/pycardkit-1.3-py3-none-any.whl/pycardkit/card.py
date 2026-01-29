class Card():
    """
    Default class for cards.
    """

    def __init__(self, rank: str, suit: str, context: dict):
        if not isinstance(context, dict):
            raise TypeError("Context must be a dict.")
        if rank not in context:
            raise ValueError(f"Invalid rank '{rank}' for the given context.")
        valid_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        if suit not in valid_suits:
            raise ValueError(f"Invalid suit '{suit}'. Must be one of {valid_suits}.")
        self.rank = rank
        self.suit = suit
        self.context = context
        self.value = context[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return f"Card('{self.rank}', '{self.suit}')"
    
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
    
    def is_face(self) -> bool:
        """
        Returns True if the card is a J, Q or K.
        """
        return self.rank.isalpha() and self.rank != "A"
    
    def is_ace(self) -> bool:
        """
        Returns True if the card is an ACE.
        """
        return self.rank == "A"
    
    def get_color(self) -> str:
        """
        Returns the color of the card: 'Red' or 'Black'.
        """
        return "Red" if self.suit in ["Hearts", "Diamonds"] else "Black"