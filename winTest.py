from Game import *
from Player import *
from copy import deepcopy

def prettyprint(s,l,d=" "):
    result = s
    for i in xrange(l - len(s)):
        result += d
    return result

game = Game("AAAA")

numPlayers = 4 #input("How many players?")
players = [Player(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[0:numPlayers]]

for player in players:
    player.joinGame("AAAA") 

game.deck.cards = [Werewolf(),DreamWolf(),Villager(),Doppleganger(),ApprenticeSeer(),ParanormalInvestigator(),Curator()]
# game.deck.shuffle()
game.deck.fillPocket()

initialPocket = deepcopy(game.deck.pocket)

for player in players:
    game.dealPlayerCard(player)#game.deck.dealOneCard())
    
for player in players:
    print "Player " + player.name + ", you were dealt the " + player.initialCard.name + " card"
    print "-------------------------------------------------------------"
    player.initialCard.nightAction()
    print ""

pocketparams = {"M":"Middle","L":"Left","R":"Right"}

game.performNightActions()
print "NAME" + "|" + prettyprint("Initial",15) + "|" + prettyprint("Final",15) + "|" + "Knowledge"
print prettyprint("",4,"-") + "+" + prettyprint("",15,"-") + "+" + prettyprint("",15,"-") + "+" + prettyprint("",10,"-")
for player in players:
    # print "Player " + player.name + ", you now know: " + player.knowledge
    print prettyprint(player.name,4) + "|" + prettyprint(player.initialCard.name,15) + "|" + prettyprint(player.finalCard.name,15) + "|" + player.knowledge
print prettyprint("",4,"-") + "+" + prettyprint("",15,"-") + "+" + prettyprint("",15,"-") + "+" + prettyprint("",10,"-")
for param in pocketparams:
    print prettyprint(param,4) + "|" + prettyprint(initialPocket[pocketparams[param]].name,15) + "|" + prettyprint(game.deck.pocket[pocketparams[param]].name,15) + "|"

print ""
print ""


game.collectVotes()
game.tallyVotes()

print "NAME" + "|" + prettyprint("Final Card",15) + "|" + prettyprint("Team",15) + "|"
print prettyprint("",4,"-") + "+" + prettyprint("",15,"-") + "+" + prettyprint("",15,"-") + "|"
for player in game.mostVoted:
    # print "Player " + player.name + ", you now know: " + player.knowledge
    print prettyprint(player.name,4) + "|" + prettyprint(player.finalCard.name,15) + "|" + prettyprint(player.finalCard.team,15) + "|"

print game.winner()