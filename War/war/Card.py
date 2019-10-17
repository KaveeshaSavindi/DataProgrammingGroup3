import random

class Card:
    def __init__(self):
        self.deck = []
        self.suit = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.value = range(1, 14)

        for v in self.value:
            if v == 1:
                v = "A"
            elif v == 11:
                v = "J"
            elif v == 12:
                v = "Q"
            elif v == 13:
                v = "K"
            for s in self.suit:
                s = (str(v) + " of " + str(s))
                self.deck.append(s)

    def shuffle(self):
        random.shuffle(self.deck)
        #Generate random number
        #randomNo = random.randint(0,51)
        #Pick a random card from Deck
        #returnCard = self.deck[randomNo]
        #Return picked card
        return (self.deck)

    def splitDeck(self):
        self.splits = []
        #Split the deck in half
        half = len(self.deck)//2
        #Store splits in a list
        for splits in range(0,1):
            self.splits.append(self.deck[:half])
            self.splits.append(self.deck[half:])
        #Return list (splits)
        return (self.splits)

#c = Card()
#c.shuffle()
#c.splitDeck()

