import random
import time
#import math
from operator import itemgetter


import class_overall
import class_weapon

    

allOptions=[["Run 8 feet to DEFENSE.",                  "OFFENSE runs 8 feet toward DEFENSE.",          "RUN"],
            ["Walk up to 4 feet toward DEFENSE.",       "OFFENSE walks toward DEFENSE.",                "WALK"],       
            ["Punch DEFENSE.",                          "OFFENSE attempts to punch DEFENSE.",           "PUNCH"],
            ["Grab DEFENSE.",                           "OFFENSE attempts to grab DEFENSE.",            "GRAB"],
            ["Draw your WEAPON and fire.",              "OFFENSE draws and shoots at DEFENSE.",         "DRAWFIRE"] ,            
            ["Draw your WEAPON and prepare your next shot.","OFFENSE draws and prepares a next shot.",  "DRAWDIG"],
            ["Fire your gun.",                          "OFFENSE attempts to shoot DEFENSE.",           "FIRE"] ,  
            ["Attempt to intimidate DEFENSE.",          "OFFENSE attempts to intimidate DEFENSE.",      "INTIM"],
            ["Spend a moment Digging Deep.",            "OFFENSE Digs Deep and prepares for action.",   "DIG"],
            ["Get help with the menu.",                 "",                                             "MENU"],
            ["Check the status of the fight.",          "",                                             "STATUS"],
            ["Quit.",                                   "",                                             "QUIT" ],
            ["Walk 2 feet away from DEFENSE.",          "OFFENSE walks 2 feet away from DEFENSE.",      "BACKAWAY"],
            ["Reload your WEAPON.",                     "OFFENSE reloads.",                             "RELOAD"],
            ["Swing with your WEAPON.",                 "OFFENSE attempts to hit DEFENSE with a saber.", "SABER"]]


allWeapons=[{'name':'six-shooter',  'range':1,  'maxbullets':6,   'sharp':0,    'isRange':True},
            {'name':'shotgun',      'range':2,  'maxbullets':3,   'sharp':10,   'isRange':True},
            {'name':'rifle',        'range':0,  'maxbullets':1,   'sharp':30,   'isRange':True},
            {'name':'saber',        'range':0,  'maxbullets':10,  'sharp':20,   'isRange':False}]

class Scenario:  #Scenario is in a very early state right now.  Eventually it will represent the various scenarios, or maps, that are selectable.
    def __init__(self):
        self.playerCount = 1
        self.playerLocations = [[16,16]]
        self.npcCount = 1
        self.npcNames = ['the banker']
        self.npcLocations = [[0,0]]
   
    def introduction(self):
        print "Welcome to Unlucky at Python"
        print
        print "You have 10 turns to rob a bank."
        print "You will succeed if you:"
        print " - Intimidate him more than he intimidates you,"
        print " - Hit him until he sustains a concussion,"
        print " - or Inflict massive damage."
        print
        print "If he out-intimidates you or you sustain"
        print "massive wounds, you will be weak enough "
        print "to be captured.  Good luck, partner!"
        
        

class Game:
    def __init__(self):
        self.players = [] #all players are added here
        self.npcs = [] #all npcs are added here
        self.weaponList = self.createWeaponList()
        
        self.scenario = Scenario()
        self.scenario.introduction()
        for x in range(self.scenario.playerCount):
            self.createPlayer()
        for x in range(self.scenario.npcCount):
            self.createNPC()
    
    def getActors(self,exclude=None):
        allActors = self.players+self.npcs
        if exclude:
            allActors.remove(exclude)
        return allActors
    actors = property(getActors)
        
    def createWeaponList(self):
        weaponList = []
        for weaponArgs in allWeapons:
            weapon=class_weapon.Weapon(**weaponArgs)
            weaponList.append(weapon)
        return weaponList
                
        
    def createPlayer(self):

        print
        self.player=class_overall.Actor(raw_input("What is your character's name?"))
        self.players.append(self.player)
        self.player.x,self.player.y = self.scenario.playerLocations.pop()
        print self.player
        print
        self.player.addRoots()
        print self.player
        print
        self.player.addWeapon(self.weaponList)
        
        
    def createNPC(self):
        npcName = self.scenario.npcNames.pop()
        print
        print "Creating stats for",npcName
        time.sleep(1)
        self.npc=class_overall.Actor(npcName, isNPC=True)
        self.npcs.append(self.npc)
        self.npc.x,self.npc.y = self.scenario.npcLocations.pop()
        self.npc.addRoots()
        print self.npc
        print
        self.npc.addWeapon(self.weaponList)
        time.sleep(1)

    def gameEnd(self): #TODO: Transition use of "player" and "npc" over to something like a loop of the "other side"
        print
        print
        if self.npc.wounddebuff<=-20:
            print self.npc.cap_name, "has sustained serious wounds and can't stop you from \n grabbing the cash.  You win!"
        elif self.player.intimcount==3:
            print "You've intimidated",self.npc.name,"into submission and make off with the cash!"
        elif self.npc.concuss<=-15:
            print self.npc.cap_name,"has sustained a concussion and sinks to the floor. You reach over him and grab the cash!"
        elif self.npc.intimcount==3:
            print self.npc.cap_name,"is far too intimidating and will never back down.  You lose!"
        elif self.player.wounddebuff<=-20:
            print "You have sustained serious wounds.  You lose!"
        elif self.roundCount>10:
            print "You've waited too long and the sheriff walks in the door.  You lose!"
        else: #if it doesn't match any of the possible game ending conditions, the game has not ended
            return False
        #if any of the above was true, return that the game is over
        return True 

    def rollInitiative(self):
        #does not handle if people roll the an identical place
        #TODO: make this code less ugly
        turnsLists = []
        for actor in self.actors:
            place = random.randint(1,10)+actor.getBonus(actor.grit)
            turnsLists.append((place,actor))
        turnsLists = sorted(turnsLists, key=itemgetter(0), reverse=True)
        turns = []
        for entry in turnsLists:
            turns.append(entry[1])
        #print 'TESTING: sorted turnsLists',turnsLists
        #print 'TESTING: sorted turns list',turns
        return turns

    def getLegalOptions(self,defense):  #builds a list of the possible options
        legalOptions=[]
        dist=self.currentActor.distanceTo(defense)
        if dist>4:
            legalOptions=[allOptions[0]] #run    
        if dist>1: 
            legalOptions.append(allOptions[1]) #walk
        if dist==1: 
            legalOptions=[allOptions[2]] #punch
        if dist==1 and defense.grapple==0: 
            legalOptions.append(allOptions[3]) #grab
        if defense.grapple==0 and self.currentActor.grapple==0:
            legalOptions.append(allOptions[12]) #back away
        if self.currentActor.weapon.isRange==True:
            if self.currentActor.weapon.bullets==0:
                legalOptions.append(allOptions[13]) #reload
            elif self.currentActor.draw==False:
                legalOptions.append(allOptions[4]) #draw and fire
                legalOptions.append(allOptions[5]) #draw and dig
            else:
                legalOptions.append(allOptions[6]) #fire
        if dist<=2 and not self.currentActor.weapon.isRange: #dist 2 probably ok?
            legalOptions.append(allOptions[14]) #saberize   
        legalOptions.append(allOptions[7]) #intimidate
        if self.currentActor.dig<=10:
            legalOptions.append(allOptions[8]) #dig deep
        if not self.currentActor.isNPC:
            legalOptions.append(allOptions[9]) #menu help
            legalOptions.append(allOptions[10]) #status
            legalOptions.append(allOptions[11]) #quit
        return legalOptions
    
    def takeTurn(self): 
        #this line is a holdover until a target system or 3+ actor support
        defense = self.getActors(exclude=self.currentActor)[0]
        
        turnOver = False
        while not turnOver:
            turnOver = True #only help and status options will cause the turn to not end.
            self.currentActor.descWounds()
            dist=self.currentActor.distanceTo(defense) 
            legalOptions=self.getLegalOptions(defense)
            if self.currentActor.isNPC:
                print self.currentActor.cap_name,"takes a turn.",
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
                    option=option.replace("OFFENSE",self.currentActor.name)
                    option=option.replace("DEFENSE",defense.name)
                    option=option.replace("DISTANCE",str(dist))
                    option=option.replace("HALF",str(dist/2))
                    option=option.replace("WEAPON",self.currentActor.weapon.name)
                    print x,".",
                    print option
                print
                turnChoice = 0
                while turnChoice not in range(1,len(legalOptions)+1): 
                    try:
                        turnChoice=input("What is your choice?")
                    except SyntaxError:
                        print "Please enter your choice by number."
                    except NameError:
                        print "Please enter your choice by number."
            
            turnText=legalOptions[turnChoice-1][1] #Types text based on option choice
            turnText=turnText.replace("OFFENSE",self.currentActor.name)
            turnText=turnText.replace("DEFENSE",defense.name)
            turnText=turnText.replace("DISTANCE",str(dist))
            turnText=turnText.replace("HALF",str(dist/2))
            turnText=turnText.replace("WEAPON",self.currentActor.weapon.name)
            print turnText
            turnAction=legalOptions[turnChoice-1][2] #Takes the action based on the choice
            if turnAction=="RUN":
                self.currentActor.moveTowards(defense,8)
            elif turnAction=="WALK":
                self.currentActor.moveTowards(defense,4)
            elif turnAction=="BACKAWAY": 
                self.currentActor.moveTowards(defense,-2)
            elif turnAction=="PUNCH":
                self.currentActor.punch(defense)
            elif turnAction=="GRAB":
                self.currentActor.grab(defense)
            elif turnAction=="RELOAD":
                self.currentActor.weapon.reload
            elif turnAction=="DRAWFIRE":
                self.currentActor.shoot(defense)
            elif turnAction=="DRAWDIG":
                self.currentActor.draw=True
                self.currentActor.dig+=5
            elif turnAction=="FIRE":
                self.currentActor.shoot(defense)
            elif turnAction=="SABER":
                self.currentActor.punch(defense)
            elif turnAction=="INTIM":
                self.currentActor.intimidate(defense)
            elif turnAction=="DIG":
                self.currentActor.dig+=10
            elif turnAction=="MENU":
                print "A high Bravery means better punches, and grabbing helps."
                print "Melee hits cause concussion damage, and each point of concussion makes\n all actions 1% less likely to succeed."
                print "Intimidation relies on your Grit and the banker's Grit. If you win the\n battle of wills you get a point,but losing subtracts a point. 3 points wins the game!"
                print "Digging Deep improves any action on your next turn by 10%. You can skip up \n to two turns this way."
                print "If you draw on the same turn you fire your gun, your are 10% less likely to hit."
                print "If you draw and wait until your next turn, your shot is 5% more likely to hit."
                print "Your accuracy with a gun relies on your Concentration."
                print
                print
                time.sleep(2)
                turnOver = False
            elif turnAction=="STATUS":
                print
                self.currentActor.showStatus()
                print
                defense.showStatus()
                print
                time.sleep(2)
                turnOver = False
            elif turnAction=="QUIT":
                self.shouldQuit = True

    def playGame(self):
        turnOrder = self.rollInitiative()
        self.shouldQuit=False
        self.roundCount=1
        turnQueue = turnOrder[:] #makes a copy instead of only referencing
        while not self.gameEnd() and not self.shouldQuit: 
            if turnQueue == turnOrder:
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print "Beginning round number ",self.roundCount,"."
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print
                time.sleep(1)
            
            self.currentActor = turnQueue.pop()

            self.takeTurn()
          
            print
            time.sleep(1)

            if not turnQueue: #if the round is empty
                self.roundCount+=1
                turnQueue = turnOrder[:]
                

        print
        print
        print 'Goodbye!'
        
game = Game()

game.playGame()
