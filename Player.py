from Game import *

class Player:
    def __init__(self,name):
        self.name = name
        self.game = None
        self.initialCard = None
        self.finalCard = None
        self.knowledge = ""
        
    def joinGame(self,gameID):
        try:
            self.game = Game.allGames[gameID]
            self.game.addPlayer(self)
        except KeyError:
            print "I'm sorry, there is no game with that ID, please try again"
    
    def updateKnowledge(self,newKnowledge):
        self.knowledge += newKnowledge
    
    def castVote(self, vote):
        self.game.votes[self.name] = vote
        