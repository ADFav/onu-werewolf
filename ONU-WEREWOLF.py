from Game import *
from Player import *

game = Game("AAAA")

numPlayers = 12 #input("How many players?")
players = [Player(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[0:numPlayers]]

for player in players:
    player.joinGame("AAAA") 

game.deck.cards = game.deck.randomHand(15)
game.deck.shuffle()
game.deck.fillPocket()

for player in players:
    game.dealPlayerCard(player,game.deck.dealOneCard())
    
for player in players:
    print "Player " + player.name + ", you were dealt the " + player.initialCard.name + " card"
    print "-------------------------------------------------------------"
    player.initialCard.nightAction()
    print ""

game.performNightActions()

for player in players:
    print "Player " + player.name + ", you now know: " + player.knowledge



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