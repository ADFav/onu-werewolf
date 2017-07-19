class Card:
    def __init__(self,cardName = "Lame-o", team = "No team!"):
        self.name = cardName
        self.team = team
        self.cardholder = None
        self.params = {}
    
    def __str__(self):
        return "Card : " + self.name + ", Team : " + self.team
        
    def nightAction(self):
        print "This card has no active night action"
        
    def performNightAction(self):
        return 0

    def game(self):
        return self.cardholder.game
    
    def deck(self):
        return self.game().deck
    
    def players(self):
        return self.game().players.keys()
        
    def getPlayer(self,playerName):
        return self.game().players[playerName]
    
    def selectPlayers(self, text = "Pick your player", notThisPlayer = []):
        tmpPlayers = [player for player in self.players() if player not in notThisPlayer]
        for player in tmpPlayers:
            print "--- " + player
        choice = raw_input(text + "\n")
        if choice in tmpPlayers:
            return self.getPlayer(choice)
        else:
            print "Not a valid choice!"
            return self.selectPlayers(text, notThisPlayer)
    
    def selectPocket(self, text, notThisCard=[]):
        tmpPocket = {pos:card for pos,card in self.deck().pocket.iteritems() if pos not in notThisCard}
        for pos in tmpPocket.keys():
            print "--- " + pos
        choice = raw_input(text + "\n")
        if choice in tmpPocket.keys():
            return choice
        else:
            print "Not a valid choice!"
            return self.selectPocket(text,notThisCard)

class Villager(Card):
    def __init__(self):
        Card.__init__(self,"Villager","Villager") 

class Hunter(Card):
    def __init__(self):
        Card.__init__(self,"Hunter","Villager")

class Tanner(Card):        
    def __init__(self):
        Card.__init__(self,"Tanner","Tanner")
        
class Mason(Card):
    def __init__(self):
        Card.__init__(self,"Mason","Villager")
    
    def performNightAction(self):
        otherMason = {name:player for name,player in self.game().players.iteritems() if player.initialCard.name == "Mason" and name != self.cardholder.name}.keys()
        if otherMason == []:
            self.cardholder.knowledge = "Sorry, there is no other mason in the game"
        else:
            if len(otherMason) == 1:
                self.cardholder.knowledge = "The other mason is " + otherMason[0] + "."
            else:
                self.cardholder.knowledge = "The other masons are " + otherMason.join(", ") + "."

class Robber(Card):
    def __init__(self):
        Card.__init__(self,"Robber", "Villager")
    
    def nightAction(self):
        self.params["victim"] = self.selectPlayers("Pick your Victim",[self.cardholder.name])
    
    def performNightAction(self):
        if self.params == {}:
            self.cardholder.knowledge = "You did not steal any card"
        else:
            mycard = self.cardholder.finalCard
            victimscard = self.params["victim"].finalCard 
            
            self.params["victim"].finalCard = mycard
            self.cardholder.finalCard = victimscard
            
            self.cardholder.knowledge = "You stole the " + victimscard.name + " card from " + self.params["victim"].name

class Troublemaker(Card):
    def __init__(self):
        Card.__init__(self,"Troublemaker", "Villager")
    
    def nightAction(self):
        self.params["victim 1"] = self.selectPlayers("Pick your First Victim",[self.cardholder.name])
        self.params["victim 2"] = self.selectPlayers("Pick your Second Victim",[self.cardholder.name, self.params["victim 1"].name])

    
    def performNightAction(self):
        if self.params == {}:
            self.cardholder.knowledge = "You did swap any cards"
        else:
            victim1card = self.params["victim 1"].finalCard
            victim2card = self.params["victim 2"].finalCard
            
            self.params["victim 1"].finalCard = victim2card
            self.params["victim 2"].finalCard = victim1card
            
            self.cardholder.knowledge = "You swapped " + self.params["victim 1"].name + "'s and " + self.params["victim 2"].name + "'s cards"

class Drunk(Card):
    def __init__(self):
        Card.__init__(self,"Drunk","Villager")
    
    def nightAction(self):
        self.params["endpoint"] = self.selectPocket("Which center card do you want to switch with?")
    
    def performNightAction(self):
        mycard = self.cardholder.finalCard
        endpoint = self.deck().pocket[self.params["endpoint"]]
        
        self.cardholder.finalcard = endpoint
        self.deck().pocket[self.params["endpoint"]] = mycard
        
        self.knowledge = "You switched your card with the " + self.params["endpoint"] + " center card."
    

class Insomniac(Card):
    def __init__(self):
        Card.__init__(self,"Insomniac","Villager")
    
    def performNightAction(self):
        self.cardholder.knowledge = "Your final card is " + self.cardholder.finalCard.name

class Seer(Card):
    def __init__(self):
        Card.__init__(self,"Seer","Villager")
    
    def nightAction(self):
        print "--- Center"
        print "--- Player"
        choice = raw_input("Where do you want to look?\n")
        if choice == "Center":
            self.params["center 1"] = self.selectPocket("Which center card would you like to see?")
            self.params["center 2"] = self.selectPocket("Which other center card would you like to see?",[self.params["center 1"]])
        elif choice == "Player":
            self.params["victim"] = self.selectPlayers("Whose card would you like to see?",[self.cardholder.name])
        else:
            print "That's an invalid choice!"
            return self.nightAction()
            
    def performNightAction(self):
        if "victim" in self.params.keys():
            self.cardholder.knowledge = "You saw that " + self.params["victim"].name + " had the " + self.params["victim"].finalCard.name + " card."
        if "center 1" in self.params.keys():
            self.cardholder.knowledge = "You looked at the " + self.params["center 1"] + " center card and saw the " + self.deck().pocket[self.params["center 1"]].name + " card, and at the " + self.params["center 2"] + " center card and saw the " + self.deck().pocket[self.params["center 2"]].name + " card."

class Werewolf(Card):
    def __init__(self):
        Card.__init__(self,"Werewolf","Werewolf")
    
    def nightAction(self):
        self.params["pocket card"] = self.selectPocket("If you are the lone wolf, which center card will you view?")
 
    def performNightAction(self):
        otherWerewolves = [player.name for player in self.game().findCardholders("Werewolf") if player.name != self.cardholder.name]
        if len(otherWerewolves) == 0:
            self.cardholder.knowledge = "There are no other werewolves in this game. When you looked in the center, you saw the " + self.params["pocket card"].name + " card"
        elif len(otherWerewolves) == 1:
            self.cardholder.knowledge = "The only other werewolf is " + otherWerewolves[0]
        else:
            self.cardholder.knowledge = "The other werewolves are " + ", ".join(otherWerewolves) + "."
        
class Minion(Card):
    def __init__(self):
        Card.__init__(self,"Minion","Werewolf")
    
    def performNightAction(self):
        werewolves = self.game().findCardholders("Werewolf")
        if len(werewolves) == 0:
            self.cardholder.knowledge = "There are no werewolves in this game"
        elif len(werewolves) == 1:
            self.cardholder.knowledge = "The only werewolf is " + werewolves[0].name
        else:
            self.cardholder.knowledge = "The werewolves are " + ", ".join(map(lambda player:player.name, werewolves)) + "."