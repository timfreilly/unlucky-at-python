import random
import time
#import math
from operator import itemgetter


import class_overall
#import class_weapon

    

allOptions=[["Run 8 feet to the banker.",    "OFFENSE runs 8 feet toward DEFENSE.", "RUN"],
            ["Walk up to 4 feet toward the banker.", "OFFENSE walks toward DEFENSE.", "WALK"],       
            ["Punch the banker.",            "OFFENSE attempts to punch DEFENSE.", "PUNCH"],
            ["Grab the banker.",             "OFFENSE attempts to grab DEFENSE.","GRAB"],
            ["Draw your gun and fire.",      "OFFENSE draws and shoots at DEFENSE.", "DRAWFIRE"] ,            
            ["Draw your gun and prepare your next shot.","OFFENSE draws and prepares the next shot.","DRAWDIG"],
            ["Fire your gun.","OFFENSE attempts to shoot DEFENSE.", "FIRE"] ,  
            ["Attempt to intimidate the banker.", "OFFENSE attempts to intimidate DEFENSE.","INTIM"],
            ["Spend a moment Digging Deep.", "OFFENSE Digs Deep and prepares for the next move.","DIG"],
            ["Get help with the menu.","", "MENU"],
            ["Check the status of the fight.","","STATUS"],
            ["Quit.", "","QUIT" ],
            ["Walk 2 feet away from the banker.", "OFFENSE walks 2 feet away from DEFENSE.", "BACKAWAY"],
            ["Reload your gun.", "OFFENSE reloads.", "RELOAD"],
            ["Slash at the banker with your saber.", "OFFENSE attempts to hit DEFENSE with a saber.", "SABER"]]

def getLegalOptions(offense,defense):  #builds a list of the possible options
    legalOptions=[]
    dist=offense.distance(defense)
    if dist>4:
        legalOptions=[allOptions[0]] #run    
    if dist>1: 
        legalOptions.append(allOptions[1]) #walk
    if dist==1: 
        legalOptions=[allOptions[2]] #punch
    if dist==1 and defense.grapple==0: 
        legalOptions.append(allOptions[3]) #grab
    if defense.grapple==0 and offense.grapple==0:
        legalOptions.append(allOptions[12]) #back away
    if offense.weapon.isRange==True:
        if offense.weapon.bullets==0:
            legalOptions.append(allOptions[13]) #reload
        elif offense.draw==False:
            legalOptions.append(allOptions[4]) #draw and fire
            legalOptions.append(allOptions[5]) #draw and dig
        else:
            legalOptions.append(allOptions[6]) #fire
    if dist<=2 and offense.weapon.special=="saber": #dist 2 probably ok?
        legalOptions.append(allOptions[14]) #saberize   
    legalOptions.append(allOptions[7]) #intimidate
    if offense.dig<=10:
        legalOptions.append(allOptions[8]) #dig deep
    if not offense.isNPC:
        legalOptions.append(allOptions[9]) #menu help
        legalOptions.append(allOptions[10]) #status
        legalOptions.append(allOptions[11]) #quit
    return legalOptions



def menuChoice(offense,defense):

    dist=offense.distance(defense) 
    legalOptions=getLegalOptions(offense,defense)
    if offense.isNPC:
        print offense.cap_name,"takes a turn.",
        count=0
        while count<=3:
            print ".",
            time.sleep(.5)
            count+=1
        print
        turnChoice=random.randint(1,len(legalOptions))
        print 
    else: # Prints a menu of legal options on the player's turn
        print "You are ",dist," feet from",defense.name+"."
        for x in range(1,len(legalOptions)+1):
            option=legalOptions[x-1][0]
            option=option.replace("DISTANCE",str(dist))
            option=option.replace("HALF",str(dist/2))
            print x,".",
            print option
        print
        try:
            turnChoice=input("What is your choice?")
        except SyntaxError:
            print "Please enter your choice by number."
            return 0 #repeats menu
        except NameError:
            print "Please enter your choice by number."
            return 0
        if turnChoice>len(legalOptions):
            print "Please enter your choice by number."
            return 0
    turnText=legalOptions[turnChoice-1][1] #Types text based on option choice
    turnText=turnText.replace("OFFENSE",offense.name)
    turnText=turnText.replace("DEFENSE",defense.name)
    turnText=turnText.replace("DISTANCE",str(dist))
    turnText=turnText.replace("HALF",str(dist/2))
    print turnText
    turnAction=legalOptions[turnChoice-1][2] #Takes the action based on the choice
    if turnAction=="RUN":
        offense.move(defense,8)
        return 1
    elif turnAction=="WALK":
        offense.move(defense,4)
        return 1
    elif turnAction=="BACKAWAY": 
        offense.move(defense,-2)
    elif turnAction=="PUNCH":
        offense.punch(defense)
        offense.dig=0
        return 1
    elif turnAction=="GRAB":
        offense.grab(defense)
        offense.dig=0
        return 1
    elif turnAction=="RELOAD":
        offense.weapon.bullets=offense.weapon.maxbullets
        return 1
    elif turnAction=="DRAWFIRE":
        offense.draw=True
        offense.drawdebuff=-10
        offense.shoot(defense)
        offense.dig=0
        offense.weapon.bullets-=1
        return 1
    elif turnAction=="DRAWDIG":
        offense.draw=True
        offense.dig+=5
        return 1
    elif turnAction=="FIRE":
        offense.shoot(defense)
        offense.dig=0
        offense.weapon.bullets-=1
        return 1
    elif turnAction=="SABER":
        offense.punch(defense)
        offense.dig=0
    elif turnAction=="INTIM":
        offense.intimidate(defense)
        offense.dig=0
        return 1
    elif turnAction=="DIG":
        offense.dig+=10
        return 1
    elif turnAction=="MENU":
        print "A high Bravery means better punches, but you must up close."
        print "If you Grab the banker, your punches are more likely to hit."
        print "Melee hits cause concussion damage, and each point of concussion makes\n all actions 1% less likely to succeed."
        print "Intimidation relies on your Grit and the banker's Grit. If you win the\n battle of wills you get a point,but losing subtracts a point. 3 points wins the game!"
        print "Digging Deep improves any action on your next turn by 10%. You can skip up \n to two turns this way."
        print "If you draw on the same turn you fire your gun, your are 10% less likely to hit."
        print "If you draw and wait until your next turn, your shot is 5% more likely to hit."
        print "Your accuracy with a gun relies on your Concentration."
        print
        print
        time.sleep(2)
        return 0
    elif turnAction=="STATUS":
        print
        offense.showStatus()
        print
        defense.showStatus()
        print
        time.sleep(2)
        return 0
    elif turnAction=="QUIT":
        return 2

def errorCatch(offense,defense):
    successfulChoice=0
    while successfulChoice==0: #errors return 0, successes return 1
        successfulChoice=menuChoice(offense,defense)
    if successfulChoice==2:
        return True  #return this value to quitChoice
    else:
        return False
   



class Scenario:
    def __init__(self):
        self.players = [] #eventually useful?
        self.npcs = [] #eventually useful?
        self.createPlayer()
        self.players.append(self.player)
        self.createNPC()
        self.npcs.append(self.npc)
        
        
    def createPlayer(self):
        print "Welcome to Unlucky at Python"
        print "You have 10 turns to rob a bank."
        print "You will succeed if you:"
        print "Intimidate him more than he intimidates you,"
        print "Hit him until he sustains a concussion,"
        print "or Inflict massive damage."
        print
        print "If he out-intimidates you or you sustain"
        print "massive wounds, you will be weak enough "
        print "to be captured.  Good luck, partner!"
        print
        self.player=class_overall.Actor(raw_input("What is your character's name?"))
        self.player.x = 16
        self.player.y = 16
        print self.player
        print
        self.player.addRoots()
        print self.player
        print
        self.player.addWeapon()
        
        
    def createNPC(self):
        print
        print "Creating stats for the banker."
        time.sleep(1)
        self.npc=class_overall.Actor("the banker", isNPC=True)
        self.npc.x = 0
        self.npc.y = 0
        self.npc.addRoots()
        print self.npc
        print
        self.npc.addWeapon()
        time.sleep(1)

    def gameEnd(self):
        print
        print
        if self.npc.wound<=-20:
            print self.npc.defense.cap_name, "has sustained serious wounds and can't stop you from \n grabbing the cash.  You win!"
        elif self.player.intimcount==3:
            print "You've intimidated",self.npc.name,"into submission and make off with the cash!"
        elif self.npc.defense.concuss<=-15:
            print self.npc.cap_name,"has sustained a concussion and sinks to the floor. You reach over him and grab the cash!"
        elif self.npc.intimcount==3:
            print self.npc.cap_name,"is far too intimidating and will never back down.  You lose!"
        elif self.player.wound<=-20:
            print "You have sustained serious wounds.  You lose!"
        elif self.roundCount>10:
            print "You've waited too long and the sheriff walks in the door.  You lose!"
        elif self.quitChoice==True:
            return True
        else: #if it doesn't match any of the possible game ending conditions, the game has not ended
            return False
        #if any of the above was true, return that the game is over
        return True 

    def rollInitiative(self):
        #does not handle if people roll the an identical place
        #TODO: make this code less ugly
        turnsLists = []
        for actor in self.players+self.npcs:
            place = random.randint(1,10)+actor.getBonus(actor.grit)
            turnsLists.append((place,actor))
        turnsLists = sorted(turnsLists, key=itemgetter(0), reverse=True)
        turns = []
        for entry in turnsLists:
            turns.append(entry[1])
        #print 'TESTING: sorted turnsLists',turnsLists
        #print 'TESTING: sorted turns list',turns
        return turns
            

    def playGame(self):
        turnOrder = self.rollInitiative()
        self.quitChoice=False
        self.roundCount=1
        turnCount = 0
        while not self.gameEnd():  #TODO: Should test thoroughly that game can end mid-turn
            if not turnCount:
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print "Beginning round number ",self.roundCount,"."
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print
                time.sleep(1)
            if turnOrder[turnCount].isNPC:
                self.npc.getWounds()
                menuChoice(self.npc,self.player)
            else:
                self.player.getWounds()
                self.quitChoice=errorCatch(self.player,self.npc)
           
            print
            time.sleep(1)

            turnCount+=1
            if turnCount==len(turnOrder):
                turnCount=0
                self.roundCount+=1

        print
        print
        print 'Goodbye!'
        
game = Scenario()

game.playGame()
