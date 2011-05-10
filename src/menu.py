import random
import time
#import math
from operator import itemgetter


import class_overall
import class_weapon
import data

    

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
            ["Swing with your WEAPON.",                 "OFFENSE attempts to hit DEFENSE with a saber.", "SABER"],
            ["Switch focus away from DEFENSE.",         "",                                             "REFOCUS"]]

class Scenario:  #Scenario is in a very early state right now.  Eventually it will represent the various scenarios, or maps, that are selectable.
    def __init__(self, title, playerCount, playerLocations, npcCount, npcNames, npcLocations, duration, weaponList, introduction):
        self.title = title
        self.playerCount = playerCount
        self.playerLocations = playerLocations
        self.npcCount = npcCount
        self.npcNames = npcNames
        self.npcLocations = npcLocations
        self.duration = duration
        self.weaponList = weaponList
        self.introduction = introduction
   
        

class Game:
    def __init__(self):
        self.players = [] #all players are added here
        self.npcs = [] #all npcs are added here
        
        self.scenario = Scenario(**data.allScenarios[0])
        print self.scenario.introduction
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
    
    def getOtherActors(self):
        allActors = self.players+self.npcs
        allActors.remove(self.currentActor)
        return allActors
    otherActors = property(getOtherActors)
        
    def createPlayer(self):

        print
        player=class_overall.Actor(raw_input("What is your character's name? "))
        self.players.append(player)
        player.x,player.y = self.scenario.playerLocations.pop()
        print player
        print
        player.addRoots()
        print player
        print
        player.addWeapon(self.scenario.weaponList)
        
        
    def createNPC(self):
        npcName = self.scenario.npcNames.pop()
        print
        print "Creating",npcName
        time.sleep(1)
        npc=class_overall.Actor(npcName, isNPC=True)
        self.npcs.append(npc)
        npc.x,npc.y = self.scenario.npcLocations.pop()
        npc.addRoots()
        print npc
        print
        npc.addWeapon(self.scenario.weaponList)
        time.sleep(1)


    def gameEnd(self): #TODO: Transition use of "player" and "npc" over to something like a loop of the "other side"
        print
        print
        
        allNPCsDisabled = True
        for npc in self.npcs:
            if not npc.isDisabled:
                allNPCsDisabled = False
        if allNPCsDisabled:
            print 'All resistance is disabled!  You make off with the cash!'
            return True
        
        allPlayersDisabled = True
        for player in self.players:
            if not player.isDisabled:
                allPlayersDisabled = False
        if allPlayersDisabled:
            print 'Your opposition is too strong. You can not complete your task!'
            return True

        if self.roundCount > self.scenario.duration:
            print 'You\'ve waited too long and the sheriff walks in the door.'
            print 'You lose!'
            return True
        return False

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

    def getLegalOptions(self):  #builds a list of the possible options
        legalOptions=[]
        dist=self.currentActor.distanceTo(self.currentActor.focus)
        if dist>4:
            legalOptions=[allOptions[0]] #run    
        if dist>1: 
            legalOptions.append(allOptions[1]) #walk
        if dist==1: 
            legalOptions=[allOptions[2]] #punch
        if dist==1 and self.currentActor.focus.grapple==0: 
            legalOptions.append(allOptions[3]) #grab
        if self.currentActor.focus.grapple==0 and self.currentActor.grapple==0:
            legalOptions.append(allOptions[12]) #back away
        if self.currentActor.weapon.type.isRange==True:
            if self.currentActor.weapon.bullets==0:
                legalOptions.append(allOptions[13]) #reload
            elif self.currentActor.draw==False:
                legalOptions.append(allOptions[4]) #draw and fire
                legalOptions.append(allOptions[5]) #draw and dig
            else:
                legalOptions.append(allOptions[6]) #fire
        if dist<=2 and not self.currentActor.weapon.type.isRange: #dist 2 probably ok?
            legalOptions.append(allOptions[14]) #saberize   
        legalOptions.append(allOptions[7]) #intimidate
        if self.currentActor.dig<=20:
            legalOptions.append(allOptions[8]) #dig deep
        if not self.currentActor.isNPC:
            if len(self.npcs) > 1: #allow focus switching, this check does not check if npcs are disabled
                legalOptions.append(allOptions[15])
            legalOptions.append(allOptions[9]) #menu help
            legalOptions.append(allOptions[10]) #status
            legalOptions.append(allOptions[11]) #quit
        return legalOptions
    
    def setFocus(self):
        if len(self.otherActors) == 1:
            self.currentActor.focus = self.otherActors[0]
            return
        if self.currentActor.isNPC:
            self.currentActor.focus = random.choice(self.players)
        else:
            print 
            print 'Please pick a target to focus on:'
            for x,actor in enumerate(self.otherActors):
                print x+1,'-',actor.cap_name
            choice = 0
            while choice not in range(1,len(self.otherActors)+1):
                try:
                    choice=input("Choose your focus: ")
                except SyntaxError:
                    print "Please enter your choice by number."
                except NameError:
                    print "Please enter your choice by number."
            self.currentActor.focus = self.otherActors[choice-1]
            print
            
            
    
    def takeTurn(self): 
        #this line is a holdover until a target system or 3+ actor support
        if not self.currentActor.focus:
            self.setFocus()
        defense = self.otherActors[0]
        
        turnOver = False
        while not turnOver:
            turnOver = True #only help and status options will cause the turn to not end.
            self.currentActor.descWounds()
            self.currentActor.state = '' #state keeps track of what the player was doing during other players' turns
            dist=self.currentActor.distanceTo(self.currentActor.focus) 
            legalOptions=self.getLegalOptions()
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
                print "You are ",dist," feet from",self.currentActor.focus.name+"."
                for x in range(1,len(legalOptions)+1):
                    option=legalOptions[x-1][0]
                    option=option.replace("OFFENSE",self.currentActor.name)
                    option=option.replace("DEFENSE",self.currentActor.focus.name)
                    option=option.replace("DISTANCE",str(dist))
                    option=option.replace("HALF",str(dist/2))
                    option=option.replace("WEAPON",self.currentActor.weapon.type.name)
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
            turnText=turnText.replace("DEFENSE",self.currentActor.focus.name)
            turnText=turnText.replace("DISTANCE",str(dist))
            turnText=turnText.replace("HALF",str(dist/2))
            turnText=turnText.replace("WEAPON",self.currentActor.weapon.type.name)
            print turnText
            turnAction=legalOptions[turnChoice-1][2] #Takes the action based on the choice
            if turnAction=="RUN":
                self.currentActor.moveTowards(self.currentActor.focus,8)
            elif turnAction=="WALK":
                self.currentActor.moveTowards(self.currentActor.focus,4)
            elif turnAction=="BACKAWAY": 
                self.currentActor.moveTowards(self.currentActor.focus,-2)
            elif turnAction=="PUNCH":
                self.currentActor.punch(self.currentActor.focus)
            elif turnAction=="GRAB":
                self.currentActor.grab(self.currentActor.focus)
            elif turnAction=="RELOAD":
                self.currentActor.weapon.reload()
            elif turnAction=="DRAWFIRE":
                self.currentActor.shoot(self.currentActor.focus)
            elif turnAction=="DRAWDIG":
                self.currentActor.draw=True
                self.currentActor.dig+=5
            elif turnAction=="FIRE":
                self.currentActor.shoot(self.currentActor.focus)
            elif turnAction=="SABER":
                self.currentActor.punch(self.currentActor.focus)
            elif turnAction=="INTIM":
                self.currentActor.intimidate(self.currentActor.focus)
            elif turnAction=="DIG":
                self.currentActor.dig+=10
            elif turnAction=="REFOCUS":
                self.setFocus()
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
                for actor in self.actors:
                    actor.showStatus()
                    print
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
            if turnQueue == turnOrder: #it is the beginning of the round
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print "Beginning round number ",self.roundCount,"."
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print
                time.sleep(1)
            
            self.currentActor = None
            while not self.currentActor:
                self.currentActor = turnQueue.pop() #the lines surrounding this line skip all players who haven't gone
                if self.currentActor.isDisabled:
                    print self.currentActor.cap_name,'is',self.currentActor.descDisabled,'and can not act!'
                    print
                    self.currentActor = False

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
