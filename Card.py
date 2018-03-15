from copy import deepcopy
import random

class Card(object):
    def __init__(self,cardName = "Lame-o", team = "No team!"):
        self.name = cardName
        self.team = team
        self.cardholder = None
        self.params = {}
        self.isWolf = False
        self.isMason = False
    
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
        
class Tanner(Card): #2 Lines    
    def __init__(self):
        Card.__init__(self,"Tanner","Tanner")

class Villager(Card): #2 Lines
    def __init__(self):
        Card.__init__(self,"Villager","Villager") 

class Hunter(Card): #2 Lines
    def __init__(self):
        Card.__init__(self,"Hunter","Villager")

class Doppleganger(Card): #16 Lines
    def __init__(self):
        Card.__init__(self,"Doppleganger","Villager")
    
    def nightAction(self):
        self.params["dopplevictim"] = self.game().selectPlayers("Whose card do you want to copy?",[self.cardholder.name])
        print "You copied the " + self.params["dopplevictim"].finalCard.name + " card from  " + self.params["dopplevictim"].name + "."
        print ""
        self.copiedCard             = deepcopy(self.params["dopplevictim"].finalCard)    
        self.team                   = self.copiedCard.team
        self.isWolf                 = self.copiedCard.isWolf
        self.isMason                = self.copiedCard.isMason
        self.copiedCard.cardholder  = self.cardholder
        self.copiedCard.nightAction()
    
    def performNightAction(self):
        self.copiedCard.performNightAction()

class Mason(Card): #13 Lines
    def __init__(self):
        Card.__init__(self,"Mason","Villager")
        self.isMason = True
        
    def performNightAction(self):
        otherMason = [player.name for player in self.game().findMasons() if player.name != self.cardholder.name]
        if otherMason == []:
            self.cardholder.updateKnowledge("Sorry, there is no other mason in the game.")
        else:
            if len(otherMason) == 1:
                self.cardholder.updateKnowledge("The other mason is " + otherMason[0] + ".")
            else:
                self.cardholder.updateKnowledge("The other masons are " + ", ".join(otherMason) + ".")

class Robber(Card): #13 Lines
    def __init__(self):
        Card.__init__(self,"Robber", "Villager")
    
    def nightAction(self):
        self.params["victim"] = self.game().selectPlayers("Pick your Victim",[self.cardholder.name])
    
    def performNightAction(self):
        if self.params == {}:
            self.cardholder.updateKnowledge("You did not steal any card.")
        else:
            mycard = self.cardholder.finalCard
            victimscard = self.params["victim"].finalCard 
            
            self.params["victim"].finalCard = mycard
            self.cardholder.finalCard = victimscard
            
            self.cardholder.updateKnowledge("You stole the " + victimscard.name + " card from " + self.params["victim"].name +".")

class Troublemaker(Card): #19 Lines
    def __init__(self):
        Card.__init__(self,"Troublemaker", "Villager")
    
    def nightAction(self):
        self.params["victim 1"] = self.game().selectPlayers("Pick your First Victim",[self.cardholder.name])
        self.params["victim 2"] = self.game().selectPlayers("Pick your Second Victim",[self.cardholder.name, self.params["victim 1"].name])

    
    def performNightAction(self):
        if self.params == {}:
            self.cardholder.updateKnowledge("You did not swap any cards.")
        else:
            victim1card = self.params["victim 1"].finalCard
            victim2card = self.params["victim 2"].finalCard
            
            self.params["victim 1"].finalCard = victim2card
            self.params["victim 2"].finalCard = victim1card
            
            self.cardholder.updateKnowledge("You swapped " + self.params["victim 1"].name + "'s and " + self.params["victim 2"].name + "'s cards.")

class Drunk(Card): #14 Lines
    def __init__(self):
        Card.__init__(self,"Drunk","Villager")
    
    def nightAction(self):
        self.params["endpoint"] = self.game().selectPocket("Which center card do you want to switch with?")
    
    def performNightAction(self):
        mycard = self.cardholder.finalCard
        endpoint = self.deck().pocket[self.params["endpoint"]]
        
        self.cardholder.finalCard = endpoint
        self.deck().pocket[self.params["endpoint"]] = mycard
        
        self.cardholder.updateKnowledge("You switched your card with the " + self.params["endpoint"] + " center card.")

class Insomniac(Card): #5 Lines
    def __init__(self):
        Card.__init__(self,"Insomniac","Villager")
    
    def performNightAction(self):
        self.cardholder.updateKnowledge("Your final card is " + self.cardholder.finalCard.name +" card.")

class Seer(Card): #23 Lines
    def __init__(self):
        Card.__init__(self,"Seer","Villager")
    
    def nightAction(self):
        print "--- Center"
        print "--- Player"
        choice = raw_input("Where do you want to look?\n")
        if choice == "Center":
            self.params["center 1"] = self.game().selectPocket("Which center card would you like to see?")
            self.params["center 2"] = self.game().selectPocket("Which other center card would you like to see?",[self.params["center 1"]])
        elif choice == "Player":
            self.params["victim"] = self.game().selectPlayers("Whose card would you like to see?",[self.cardholder.name])
        else:
            print "That's an invalid choice!"
            return self.nightAction()
            
    def performNightAction(self):
        if self.params == {}:
            self.cardholder.updateKnowledge("You did not look at any cards.")
        if "victim" in self.params.keys():
            self.cardholder.updateKnowledge("You saw that " + self.params["victim"].name + " had the " + self.params["victim"].finalCard.name + " card.")
        if "center 1" in self.params.keys():
            self.cardholder.updateKnowledge("You looked at the " + self.params["center 1"] + " center card and saw the " + self.deck().pocket[self.params["center 1"]].name + " card, and at the " + self.params["center 2"] + " center card and saw the " + self.deck().pocket[self.params["center 2"]].name + " card.")

class Werewolf(Card): #26 Lines
    def __init__(self):
        Card.__init__(self,"Werewolf","Werewolf")
        self.isWolf = True
    
    def nightAction(self):
        self.params["pocket card"] = self.game().selectPocket("If you are the lone wolf, which center card will you view?")
 
    def performNightAction(self):
        otherWerewolves = [player.name for player in self.game().findWolves() if player.name != self.cardholder.name]
        if len(otherWerewolves) == 0:
            self.cardholder.updateKnowledge("There are no other werewolves in this game.")
            if "pocket card" in self.params:
                self.cardholder.updateKnowledge(" When you looked at the " + self.params["pocket card"] + " center, you saw the " + self.deck().pocket[self.params["pocket card"]].name + " card.")
            if self.params == {}:
                self.cardholder.updateKnowledge(" You did not look at any center cards.")
        elif len(otherWerewolves) == 1:
            self.cardholder.updateKnowledge("The only other werewolf is " + otherWerewolves[0] +".")
        else:
            self.cardholder.updateKnowledge("The other werewolves are " + ", ".join(otherWerewolves) + ".")
        
        dreamWolves = [player.name for player in self.game().findWolves() if player.finalCard.name == "Dream Wolf"]
        if dreamWolves != []:
            if len(dreamWolves) == 1:
                self.cardholder.updateKnowledge(" " + dreamWolves[0] + " is a Dream Wolf")
            else:
                self.cardholder.updateKnowledge(" " + ", ".join(dreamWolves) + " are Dream Wolves.")
        
class Minion(Card): #11 Lines
    def __init__(self):
        Card.__init__(self,"Minion","Werewolf")
    
    def performNightAction(self):
        werewolves = self.game().findWolves()
        if len(werewolves) == 0:
            self.cardholder.updateKnowledge("There are no werewolves in this game.")
        elif len(werewolves) == 1:
            self.cardholder.updateKnowledge("The only werewolf is " + werewolves[0].name + ".")
        else:
            self.cardholder.updateKnowledge("The werewolves are " + ", ".join([player.name for player in werewolves]) + ".")

##Begin Daybreak Roles##

#Sentinel
#BodyGuard
#AlphaWolf
#VillageIdiot

class Witch(Card): #15 Lines
    def __init__(self):
        Card.__init__(self,"Witch","Villager")
    
    def nightAction(self):
        self.params["center card"] = self.game().selectPocket("Which center card do you want to take?")
        self.params["victim"]      = self.game().selectPlayers("Who do you want to give that card to?",[self.cardholder.name])
    
    def performNightAction(self):
        centercard =  self.game().deck.pocket[self.params["center card"]]
        victimscard = self.params["victim"].finalCard
        
        self.params["victim"].finalCard = centercard
        self.game().deck.pocket[self.params["center card"]] = victimscard
        
        self.cardholder.updateKnowledge("You took the " + centercard.name + " card from the " + self.params["center card"] + " center card, and gave it to " + self.params["victim"].name + ".")

class MysticWolf(Werewolf): #11 Lines
    def __init__(self):
        Card.__init__(self,"Mystic Wolf","Werewolf")
        self.isWolf = True
    
    def nightAction(self):
        super(MysticWolf,self).nightAction()
        self.params["victim"] = self.game().selectPlayers("Whose card do you want to look at?",[self.cardholder.name])
    
    def performNightAction(self):
        super(MysticWolf,self).performNightAction()
        self.cardholder.updateKnowledge(" You looked at " + self.params["victim"].name + "'s card, and saw they had the " + self.params["victim"].finalCard.name + " card.")

class DreamWolf(Card): #3 Lines
    def __init__(self):
        Card.__init__(self,"Dream Wolf","Werewolf")
        self.isWolf = True

class ParanormalInvestigator(Card): #21 Lines
    def __init__(self):
        Card.__init__(self,"Paranormal Investigator","Villager")
    
    def nightAction(self):
        self.params["victim 1"] = self.game().selectPlayers("Choose your first victim",[self.cardholder.name])
        self.params["victim 2"] = self.game().selectPlayers("Choose your second victim",[self.cardholder.name,self.params["victim 1"].name])
    
    def performNightAction(self):
        self.cardholder.updateKnowledge(" ")
        if self.params["victim 1"].finalCard.team == "Villager":
            self.cardholder.updateKnowledge("You looked at " + self.params["victim 1"].name + "'s card and saw the " + self.params["victim 1"].finalCard.name + " card.")
            if self.params["victim 2"].finalCard.team == "Villager":
                self.cardholder.updateKnowledge(" You looked at " + self.params["victim 2"].name + "'s card and saw the " + self.params["victim 2"].finalCard.name + " card.")
            else:
                self.cardholder.updateKnowledge(" You looked at " + self.params["victim 2"].name + "'s card and saw the " + self.params["victim 2"].finalCard.name + " card. You have now joined the " + self.params["victim 2"].finalCard.team + " team.")
                self.team = self.params["victim 2"].finalCard.team
                self.isWolf = self.params["victim 2"].finalCard.isWolf
        else:
            self.cardholder.updateKnowledge(" You looked at " + self.params["victim 1"].name + "'s card and saw the " + self.params["victim 1"].finalCard.name + " card. You have now joined the " + self.params["victim 1"].finalCard.team + " team.")
            self.team = self.params["victim 1"].finalCard.team
            self.isWolf = self.params["victim 1"].finalCard.isWolf

class Revealer(Card): #11 Lines
    def __init__(self):
        Card.__init__(self,"Revealer","Villager")
    
    def nightAction(self):
        self.params['victim'] = self.game().selectPlayers("Whose card do you want to reveal?",[self.cardholder.name])
    
    def performNightAction(self):
        if self.params["victim"].finalCard.team == "Villager" or self.params["victim"].finalCard.name in ["Doppleganger", "Paranormal Investigator"]:
            map(lambda x: x.updateKnowledge(" " + self.params['victim'].name +" has been revealed to have the " + self.params["victim"].finalCard.name + " card.") , [player for player in self.game().players.values()])
        else:
            self.cardholder.updateKnowledge("You revealed " + self.params['victim'].name +" to have the " + self.params["victim"].finalCard.name + " card. But you couldn't reveal that knowledge to the rest of the players")
            
class ApprenticeSeer(Card): #8 Lines
    def __init__(self):
        Card.__init__(self,"Apprentice Seer","Villager")
    
    def nightAction(self):
        self.params["center"] = self.game().selectPocket("Which center card would you like to see?")
            
    def performNightAction(self):
        self.cardholder.updateKnowledge("You looked at the " + self.params["center"] + " center card and saw the " + self.deck().pocket[self.params["center"]].name + " card.")

class Curator(Card): #28 Lines
    def __init__(self):
        Card.__init__(self,"Curator","Villager")
    
    def nightAction(self):
        self.params["victim"] = self.game().selectPlayers("Who would you like to give an artifact to?",[self.cardholder.name])
    
    def performNightAction(self):
        random.shuffle(self.game().artifacts)
        artifact = self.game().artifacts.pop()
        map(lambda player : player.updateKnowledge(" " + self.params["victim"].name + " has an artifact token."),[player for player in self.game().players.values() if player != self.params["victim"]])
        if artifact == "Werewolf":
            self.params["victim"].finalCard.team = "Werewolf"
            self.params["victim"].finalCard.isWolf = True
            self.params["victim"].updateKnowledge(" You have been given the Claw of the Werewolf Artifact. You are now a werewolf.")
        if artifact == "Villager":
            self.params["victim"].finalCard.team = "Villager"
            self.params["victim"].finalCard.isWolf = False
            self.params["victim"].updateKnowledge(" You have been given the Brand of the Villager Artifact. You are now a villager.")
        if artifact == "Tanner":
            self.params["victim"].finalCard.team = "Tanner"
            self.params["victim"].finalCard.isWolf = False
            self.params["victim"].updateKnowledge(" You have been given the Cudgel of the Tanner Artifact. You are now a tanner.")
        if artifact == "Nothingness":
            self.params["victim"].updateKnowledge(" You have been given the Void of Nothingness Artifact. Nothing happens to you.")
        if artifact == "Shame":
            self.params["victim"].updateKnowledge(" You have been given the Mask of Muting Artifact. You may not speak for the rest of the game.")
        if artifact == "Muting":
            self.params["victim"].updateKnowledge(" You have been given the Shroud of Shame Artifact. You must turn your back on the rest of the players for this game.")    