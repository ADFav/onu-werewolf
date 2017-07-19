from Card import *
import random

class Deck:
    possibleCards = [Werewolf(), Werewolf(), Minion(), Drunk(), Seer(), Villager(),Villager(),Villager(),Mason(),Mason(),Hunter(),Tanner(),Robber(),Troublemaker(),Insomniac()]
    def __init__(self):
        self.cards = []
        self.pocket = {"Left":None, "Middle":None, "Right":None}
        self.dealCount = 0
    
    def addCard(self, card):
        self.cards.append(card)
        
    def removeCard(self,card):
        self.cards.remove(card)
    
    def randomHand(self,numCards):
        return random.sample(Deck.possibleCards,numCards)
        # for card in self.cards:
        #     print card.name 
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def dealOneCard(self):
        self.dealCount += 1
        return self.cards[self.dealCount-1]
    
    def fillPocket(self):
        self.pocket["Left"] = self.dealOneCard()
        self.pocket["Middle"] = self.dealOneCard()
        self.pocket["Right"] = self.dealOneCard()
    
        