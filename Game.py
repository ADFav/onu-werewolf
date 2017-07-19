# from Player import *
from random import choice
from Deck import *

class Game:
    allGames = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    def __init__(self, gameID=None):
        if gameID == None:
            self.gameID = self.generateGameID()  
        else:
            self.gameID = gameID
        Game.allGames[self.gameID] = self
        self.players = {}
        self.deck = Deck()
    
    def __del__(self):
        return 0
        
    def generateGameID(self):
        result = choice(Game.letters) + choice(Game.letters) + choice(Game.letters) + choice(Game.letters)
        if result in Game.allGames:
            return self.generateGameID()
        else:
            return result
        
    def addPlayer(self,player):
        self.players[player.name] = player
    
    def listAllPlayers(self):
        for player in self.players:
            print player
        return 0
        
    def dealPlayerCard(self,player,card):
        player.initialCard = card
        player.finalCard   = card
        card.cardholder = player
    
    def findCardholders(self, cardName = None):
        return [player for player in self.players.values() if player.initialCard.name == cardName]

    def performNightActions(self, cardName = None):
        if cardName != None:
            map(lambda player: player.initialCard.performNightAction(), self.findCardholders(cardName))
        else:
            map(lambda role: self.performNightActions(role), ["Doppleganger","Werewolf","Minion","Mason","Seer","Robber","Troublemaker","Drunk","Insomniac"])
    
    def endGame(self):
        Game.allGames.pop(self.gameID,None)
        for player in self.players:
            player.game = None
        self.__del__()