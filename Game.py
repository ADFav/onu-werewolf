# from Player import *
from random import choice
from Deck import *

class Game:
    allGames = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    nightOrder = ["Doppleganger","Werewolf","Mystic Wolf","Minion","Mason","Seer","Apprentice Seer","Witch","Paranormal Investigator","Robber","Troublemaker","Drunk","Insomniac","Revealer","Curator"]
    
    def __init__(self, gameID=None):
        if gameID == None:
            self.gameID = self.generateGameID()  
        else:
            self.gameID = gameID
        Game.allGames[self.gameID] = self
        self.players = {}
        self.deck = Deck()
        self.votes = {}
        self.mostVoted = []
        self.artifacts = ["Muting","Shame","Nothingness","Werewolf","Tanner","Villager"]
    
        
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
        
    def dealPlayerCard(self,player):
        card = self.deck.dealOneCard()
        player.initialCard = card
        player.finalCard   = card
        card.cardholder = player
    
    def findCardholders(self, cardName = None):
        return [player for player in self.players.values() if player.initialCard.name == cardName]

    def performNightActions(self, cardName = None):
        if cardName != None:
            map(lambda player: player.initialCard.performNightAction(), self.findCardholders(cardName))
        else:
            map(lambda role: self.performNightActions(role), Game.nightOrder)
    
    def selectPlayers(self, text = "Pick your player", notThisPlayer = []):
        tmpPlayers = [player for player in self.players if player not in notThisPlayer]
        for player in tmpPlayers:
            print "--- " + player
        choice = raw_input(text + "\n")
        if choice in tmpPlayers:
            return self.players[choice]
        else:
            print "Not a valid choice!"
            return self.selectPlayers(text, notThisPlayer)
    
    def selectPocket(self, text, notThisCard=[]):
        tmpPocket = {pos:card for pos,card in self.deck.pocket.iteritems() if pos not in notThisCard}
        for pos in tmpPocket.keys():
            print "--- " + pos
        choice = raw_input(text + "\n")
        if choice in tmpPocket.keys():
            return choice
        else:
            print "Not a valid choice!"
            return self.selectPocket(text,notThisCard)
    
    def collectVotes(self):
        for player in self.players.values():
            player.castVote(self.selectPlayers("Player " + player.name + ", cast your vote.").name)
    
    def tallyVotes(self):
        voteTally = {player:self.votes.values().count(player) for player in self.players}
        self.mostVoted = [self.players[player] for player in voteTally if voteTally[player] == max(voteTally.values())]
        if max(voteTally.values()) == 1:
            self.mostVoted = []
        
    def winner(self):
        self.mostVoted = [player if player.finalCard.name != "Hunter" else self.players[self.votes[player.name]] for player in self.mostVoted]
        killedWolves   = [player for player in self.mostVoted        if player.finalCard.isWolf]
        wolvesInGame   = [player for player in self.players.values() if player.finalCard.isWolf]
        killedTanners  = [player for player in self.mostVoted        if player.finalCard.team == "Tanner"]
        killedMinions  = [player for player in self.mostVoted        if player.finalCard.name == "Minion"]
        minionsInGame  = [player for player in self.players.values() if player.finalCard.name == "Minion"]
        result = set([])
        
        if killedTanners != []:
            result.add("Tanner")
        if self.mostVoted == [] and wolvesInGame == []:
            result.add("Villagers")
        if killedWolves != []:
            result.add("Villagers")
        if wolvesInGame != [] and killedWolves == [] and killedTanners == []:
            result.add("Werewolves")
        if wolvesInGame == [] and minionsInGame != [] and self.mostVoted != [] and killedMinions == [] and killedTanners == []:
            result.add("Werewolves")
        return result
    
    def findWolves(self):
        return [player for player in self.players.values() if player.finalCard.isWolf]
    
    def findMasons(self):
        return [player for player in self.players.values() if player.finalCard.isMason]
    
    def endGame(self):
        Game.allGames.pop(self.gameID,None)
        for player in self.players:
            player.game = None
        self.__del__()