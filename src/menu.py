import random
import time
import copy
from operator import itemgetter


import class_overall
import class_weapon
import data

    

allOptions=[["Run 8 feet to DEFENSE.",                  "OFFENSE runs 8 feet toward DEFENSE.",          "self.currentActor.moveTowards(self.currentActor.focus,8)"],
            ["Walk up to 4 feet toward DEFENSE.",       "OFFENSE walks toward DEFENSE.",                "self.currentActor.moveTowards(self.currentActor.focus,4)"],       
            ["Punch DEFENSE.",                          "OFFENSE attempts to punch DEFENSE.",           "self.currentActor.punch(self.currentActor.focus)"],
            ["Grab DEFENSE.",                           "OFFENSE attempts to grab DEFENSE.",            "self.currentActor.grab(self.currentActor.focus)"],
            ["Draw your WEAPON and fire.",              "OFFENSE draws and shoots at DEFENSE.",         "self.currentActor.shoot(self.currentActor.focus)"] ,            
            ["Draw your WEAPON and prepare your next shot.","OFFENSE draws and prepares a next shot.",  "self.currentActor.draw()"],
            ["Fire your WEAPON.",                       "OFFENSE attempts to shoot DEFENSE.",           "self.currentActor.shoot(self.currentActor.focus)"] ,  
            ["Attempt to intimidate DEFENSE.",          "OFFENSE attempts to intimidate DEFENSE.",      "self.currentActor.intimidate(self.currentActor.focus)"],
            ["Spend a moment Digging Deep.",            "OFFENSE Digs Deep and prepares for action.",   "self.currentActor.dig()"],
            ["Get help with the menu.",                 "",                                             "self.showGuide()"],
            ["Check the status of the fight.",          "",                                             "self.showActors()"],
            ["Quit.",                                   "",                                             "self.shouldQuit = True" ],
            ["Walk 2 feet away from DEFENSE.",          "OFFENSE walks 2 feet away from DEFENSE.",      "self.currentActor.moveTowards(self.currentActor.focus,-2)"],
            ["Reload your WEAPON.",                     "OFFENSE reloads.",                             "self.currentActor.reload()"],
            ["Swing with your WEAPON.",                 "OFFENSE attempts to hit DEFENSE with a saber.", "self.currentActor.swing(self.currentActor.focus)"],
            ["Switch focus away from DEFENSE.",         "",                                             "self.setFocus()"],
            ["Escape from GRABBER's hold",              "OFFENSE struggles against GRABBER's hold.",    "self.currentActor.escape()"]]


class Scenario:  #Scenario is in a very early state right now.  Eventually it will represent the various scenarios, or maps, that are selectable.
    def __init__(self, title, actors, teams, events, endConditions, introduction):
        self.title = title
        self.actors = actors
        self.teams = teams
        self.events = events
        self.endConditions = endConditions
        self.introduction = introduction
   
        

class Battle:
    def __init__(self,scenarioChoice):
        self.actors = []
        self.scenario = Scenario(**data.allScenarios[scenarioChoice])
        print self.scenario.introduction
        for partialActor in self.scenario.actors:
            self.createActor(partialActor)
        
    def showActors(self):
        self.turnOver = False
        print
        for actor in self.actors:
            actor.showStatus()
            print
            print
        time.sleep(2)
        
    def showGuide(self):
        self.turnOver = False
        print "High Bravery or a successful grab aids melee strikes."
        print "Melee hits aren't as sharp as bullets, but concussion does add up."
        print "Your accuracy with a gun relies on your Concentration."        
        print "Intimidation relies on your Grit."
        print "Winning a battle of wills may push your opponent to cower in fear."
        print "Digging Deep improves your next action by 20%."
        print "If you draw on the same turn you shoot, you are less likely to hit."
        print
        print
        time.sleep(2)
    
    def createActor(self,partialActor):
        name = partialActor['name'] if 'name' in partialActor else raw_input('What is your character\'s name?')
        actor = class_overall.Actor(name,partialActor['isNPC'])
        self.actors.append(actor)
        actor.x, actor.y = partialActor['location']
        actor.team = partialActor['team']
        print actor
        print
        actor.addRoots()
        print
        for team in self.scenario.teams:        #Not totally satisfied with this code, which looks through the teams to get to the weaponList
            if team['name'] == actor.team:
                actor.addWeapon(team['weaponList'])
        time.sleep(1)


    def gameEnd(self): 
        #TODO: doesn't belong in "gameEnd" but good enough for now
        for event in self.scenario.events:
            if eval(event['condition']):
                for action in event['actions']:
                    eval(action)
                del self.scenario.events[self.scenario.events.index(event)]

        for team in self.scenario.teams:
            standing = len([actor for actor in self.actors if actor.team == team['name'] and not actor.isDisabled])  #list comprehension, heck yeah!
            
            if standing==0:
                print team['defeatMessage']
                return True
        for condition in self.scenario.endConditions:
            if eval(condition):
                print self.scenario.endConditions[condition]
                return True
        return False

    def getLegalOptions(self):  #builds a list of the possible options
        legalOptions=[]
        dist=self.currentActor.distanceTo(self.currentActor.focus)
        if 'GRABBED' not in self.currentActor.flags:
            if dist>4:
                legalOptions.append(allOptions[0]) #run    
            if dist>1: 
                legalOptions.append(allOptions[1]) #walk
            legalOptions.append(allOptions[12]) #back away
        else:
            legalOptions.append(allOptions[16]) #escape grapple
        if dist==1: 
            legalOptions.append(allOptions[2]) #punch
        if dist==1 and 'GRABBED' not in self.currentActor.flags + self.currentActor.focus.flags: 
            legalOptions.append(allOptions[3]) #grab
        if self.currentActor.weapon.type.isRange==True:
            if self.currentActor.weapon.bullets==0:
                if self.currentActor.gear.ammoCount(self.currentActor.weapon.type):
                    legalOptions.append(allOptions[13]) #reload
            elif self.currentActor.weapon.drawn==False:
                legalOptions.append(allOptions[4]) #draw and fire
                legalOptions.append(allOptions[5]) #draw and dig
            else:
                legalOptions.append(allOptions[6]) #fire
        if dist<=2 and not self.currentActor.weapon.type.isRange: #dist 2 probably ok?
            legalOptions.append(allOptions[14]) #saberize   
        legalOptions.append(allOptions[7]) #intimidate
        if 'DIGGING' not in self.currentActor.flags:
            legalOptions.append(allOptions[8]) #dig deep
        if not self.currentActor.isNPC:
            if len([actor for actor in self.actors if actor.team != self.currentActor.team and not actor.isDisabled]) > 1: 
                legalOptions.append(allOptions[15])
            legalOptions.append(allOptions[9]) #menu help
            legalOptions.append(allOptions[10]) #status
            legalOptions.append(allOptions[11]) #quit
        return legalOptions
    
    def setFocus(self):
        self.turnOver = False
        otherTeam = [actor for actor in self.actors if actor.team != self.currentActor.team and not actor.isDisabled]
        if self.currentActor.isNPC:
            self.currentActor.focus = random.choice(otherTeam)
        else:
            if len(otherTeam)==1:
                self.currentActor.focus = otherTeam[0]
            else:
                if self.currentActor.focus and 'GRABBING' in self.currentActor.flags:
                    print
                    print 'Changing focus will release your grab.  Continue?'
                    print '1 - Yes'
                    print '2 - No'
                    choice = 0
                    while choice not in (1,2):
                        try:
                            choice = input("Enter your choice ")
                        except SyntaxError:
                            print "Please enter your choice by number."
                        except NameError:
                            print "Please enter your choice by number."
                    if choice == 1:
                        self.currentActor.breakGrapple()
                    else:
                        print
                        return
                print 
                print 'Please pick a target to focus on:'
                for x,actor in enumerate(otherTeam):
                    print x+1,'-',actor.cap_name
                choice = 0
                while choice not in range(1,len(otherTeam)+1):
                    try:
                        choice=input("Choose your focus: ")
                    except SyntaxError:
                        print "Please enter your choice by number."
                    except NameError:
                        print "Please enter your choice by number."
                self.currentActor.focus = otherTeam[choice-1]
                print
            
            
    
    def takeTurn(self): 
        #this line is a holdover until a target system or 3+ actor support
        if not self.currentActor.focus:
            self.setFocus()
        if self.currentActor.focus.isDisabled: #is your grab target disabled?
            if self.currentActor.grappleActor:
                self.currentActor.breakGrapple()
            self.setFocus()
        
        self.turnOver = False
        while not self.turnOver: #some actions do not end the turn: changing focus, checking status, getting help
            self.turnOver = True #only help and status options will cause the turn to not end.
            print self.currentActor.descState()+'.'
            self.currentActor.clearBasicFlags() #basic flags are one-turn flags: MOVINGSLOW, MOVINGFAST, DRAWING
            dist=self.currentActor.distanceTo(self.currentActor.focus) 
            legalOptions=self.getLegalOptions()
            if self.currentActor.isNPC:
                print self.currentActor.cap_name,"takes a turn.",
                for x in range(3):
                    print ".",
                    time.sleep(.5)
                print
                turnChoice=random.randint(1,len(legalOptions))
                print 
            else: # Prints a menu of legal options on the player's turn
                if 'GRABBING' in self.currentActor.flags:
                    print 'You are grabbing',self.currentActor.grappleActor.name
                elif 'GRABBED' in self.currentActor.flags:
                    print 'You are grabbed by',self.currentActor.grappleActor.name
                else:
                    print "You are ",dist," feet from",self.currentActor.focus.name+"."
                for x in range(1,len(legalOptions)+1):
                    option=legalOptions[x-1][0]
                    option=option.replace("OFFENSE",self.currentActor.name)
                    option=option.replace("DEFENSE",self.currentActor.focus.name)
                    option=option.replace("DISTANCE",str(dist))
                    option=option.replace("HALF",str(dist/2))
                    option=option.replace("WEAPON",self.currentActor.weapon.type.name)
                    if 'GRABBED' in self.currentActor.flags:
                        option=option.replace("GRABBER",self.currentActor.grappleActor.name)
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
            if 'GRABBED' in self.currentActor.flags:
                turnText=turnText.replace("GRABBER",self.currentActor.grappleActor.name)
            print turnText
            turnAction=legalOptions[turnChoice-1][2] #Takes the action based on the choice
            exec turnAction


    def startBattle(self):
        for actor in self.actors:
            actor.rollInitiative()
        self.shouldQuit=False
        self.roundCount=1
        turn = 100 #The game "counts down" from 100 and each actor gets a turn whenever their number comes up
        while not self.gameEnd() and not self.shouldQuit: 
            if turn == 100:
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print "Beginning round number ",self.roundCount,"."
                print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
                print
                time.sleep(1)

            for actor in self.actors:
                if actor.initiative == turn:
                    if actor.isDisabled:
                        print actor.descState(),'and can not act!'
                    else:
                        self.currentActor = actor #TODO: Should this just be a parameter?
                        self.takeTurn()
                    print
                    print
                    time.sleep(1)

            turn -= 1
            if turn == -100:
                self.roundCount+=1
                turn = 100

                

        print
        print
        print 'Goodbye!'

class Game:
    def __init__(self):
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        print '^^^^  UNLUCKY AT CARDS  ^^^^^'
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        print 
        scenarioChoice = self.pickScenario()
        print
        battle = Battle(scenarioChoice)
        battle.startBattle()
        
    def pickScenario(self):
        scenarioChoice = 0
        print
        print 'Choose a scenario:'
        for x,scene in enumerate(data.allScenarios):
            print str(x+1)+'.',scene['title']
        while scenarioChoice < 1 or scenarioChoice > len(data.allScenarios):
            try:
                print
                scenarioChoice=input("Enter your choice ")
            except SyntaxError:
                print "Please enter your choice by number."
            except NameError:
                print "Please enter your choice by number."
        return scenarioChoice - 1


game = Game()