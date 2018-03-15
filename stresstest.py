from Game import *
from Player import *
import random

for i in xrange(10000):
    Game()

for i in xrange(70000):
    Player(i).joinGame(random.choice(Game.allGames.keys()))

# for game in Game.allGames.values():
#     try:
#         game.deck.cards = game.deck.randomHand(3+len(game.players))
#         game.deck.fillPocket()
#         for player in game.players.values():
#             game.dealPlayerCard(player,game.deck.dealOneCard())
#     except ValueError:
#         print "whoops, too many people in that game"