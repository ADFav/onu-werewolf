from Game import *
from Player import *
from copy import *

def prettyprint(s,l,d=" "):
    result = s
    for i in xrange(l - len(s)):
        result += d
    return result

game = Game("AAAA")

numPlayers = 12 #input("How many players?")
players = [Player(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[0:numPlayers]]

for player in players:
    player.joinGame("AAAA") 

game.deck.cards = game.deck.randomHand(15)
game.deck.shuffle()
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

# cardSelect = None
# while(cardSelect != "x"):
#     for i in xrange(len(Deck.possibleCards)):
#         if Deck.possibleCards[i] in g.deck.cards:
#             print str(i+1) + ". *********"
#         else:
#             print str(i+1) + ". " + Deck.possibleCards[i].name
#     cardSelect = raw_input("Which cards should we play with? Use the numbers to select, or negative that number to remove. When done, type in 'x'")
#     if cardSelect == "x":
#         print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#         if len(g.deck.cards) > numPlayers + 3:
#             cardSelect = None
#             print "You have selected too many cards. Please remove some"
#         if len(g.deck.cards) < numPlayers + 3:
#             cardSelect = None
#             print "You have not selected enough card. Please add some"
#     else:
#         try:
#             cardSelect = int(cardSelect)
#             if int(cardSelect) > 0 and Deck.possibleCards[cardSelect-1] not in g.deck.cards:
#                 g.deck.addCard(Deck.possibleCards[cardSelect-1])
#             if int(cardSelect) < 0 and Deck.possibleCards[-1-cardSelect] in g.deck.cards:
#                 g.deck.removeCard(Deck.possibleCards[-1-cardSelect])
#         except ValueError:
#             print "That was not a valid number choice. Please try again."