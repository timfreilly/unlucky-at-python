import random
import time
import copy
from operator import itemgetter
import pickle


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
            ["Flee.",                                   "",                                             "self.currentActor.flee()" ],
            ["Walk 2 feet away from DEFENSE.",          "OFFENSE walks 2 feet away from DEFENSE.",      "self.currentActor.moveTowards(self.currentActor.focus,-2)"],
            ["Reload your WEAPON.",                     "OFFENSE reloads.",                             "self.currentActor.reload()"],
            ["Swing with your WEAPON.",                 "OFFENSE attempts to hit DEFENSE with a saber.", "self.currentActor.swing(self.currentActor.focus)"],
            ["Switch focus away from DEFENSE.",         "",                                             "self.setFocus()"],
            ["Escape from GRABBER's hold",              "OFFENSE struggles against GRABBER's hold.",    "self.currentActor.escape()"]]


class Team:
    def __init__(self, name, weaponList, defeatMessage):
        self.members = []
        self.name = name
        self.weaponList = weaponList
        self.defeatMessage = defeatMessage
        
    def __len__(self):
        return len(self.members)
        
    def isPlayerTeam(self):
        return True if len([actor for actor in self.members if not actor.isNPC]) else False
    
    def getStandingMembers(self):
        return [actor for actor in self.members if not actor.isDisabled and not actor.isHidden]
    standingMembers = property(getStandingMembers)
    
class Event:
    def __init__(self, condition, actions):
        self.condition = condition
        self.actions = actions

class Scenario:  
    def __init__(self, scenarioData, player=None):
        self.actors = []
        self.teams = {} #key:value is string name:instance
        self.events = []
        for team in scenarioData['teams']:
            newTeam = Team(team['name'],team['weaponList'],team['defeatMessage'])
            self.teams[team['name']] = newTeam #add a new dictionary entry with that team name with the value being the reference
        
        
        for partialActor in scenarioData['actors']:
            if not partialActor['isNPC'] and player: #if the player file was loaded and we've found a player slot in the scenario, load him instead of new
                newActor = player
                newActor.team = self.teams[partialActor['team']]
                newActor.isHidden = False
            else:
                name = partialActor['name']  
                newActor = class_overall.Actor(name,partialActor['isNPC'],partialActor['isHidden'])
                newActor.addRoots()
                print
                newActor.team = self.teams[partialActor['team']]
                newActor.addWeapon(newActor.team.weaponList)
            
            newActor.x, newActor.y = partialActor['location']
            self.actors.append(newActor)
            self.teams[partialActor['team']].members.append(newActor)
        
        for event in scenarioData['events']:
            newEvent = Event(event['condition'],event['actions'])
            self.events.append(newEvent)
        
        print scenarioData['introduction']
        time.sleep(3)
        battle = Battle(self.actors, self.teams, self.events)
        battle.startBattle()
        
        self.result = battle.result #straight pass-through for now
        
        player = next(actor for actor in battle.actors if not actor.isNPC)
        self.cleanPlayer(player)
        print
        print
        print 'Goodbye!'
   
    def cleanPlayer(self, player):
        player.team = None
        player.flags = []
        player.focus = None
        player.losthp = 0
        self.finalPlayer = player
        
        
   

class Battle:
    def __init__(self, actors, teams, events):
        self.actors = actors
        self.teams = teams
        self.events = events
        self.result = None
        
    def showActors(self):
        self.turnOver = False
        print
        for actor in [actor for actor in self.actors if not actor.isHidden]:
            actor.showStatus()
            print
            print
        time.sleep(2)
        
    def showGuide(self):
        self.turnOver = False
        print "High Bravery or a successful grab aids melee strikes."
        print "Melee hits aren't as sharp as bullets, but concussion does add up."
        print "Your accuracy with a gun relies on your Concentration."
        print "If you draw on the same turn you shoot, you are less likely to hit."        
        print "Intimidation relies on your Grit."
        print "Winning a battle of wills may push your opponent to cower in fear."
        print "Digging Deep improves your next action by 20%."
        print
        print
        time.sleep(2)


    def gameEnd(self): 
        #TODO: doesn't belong in "gameEnd" but good enough for now
        for event in self.events:
            if eval(event.condition):
                for action in event.actions:
                    eval(action)
                    if self.result: #if result has been changed, the battle should end.
                        return True
                del self.events[self.events.index(event)]
        for team in self.teams.values():
            if not team.standingMembers:
                self.endBattle(team.defeatMessage, not team.isPlayerTeam)
                return True
        return False
    
    def endBattle(self,message,victory): #this is barely useful
        print message
        self.result = 'win' if victory else 'loss'
    
    def revealActor(self,actorName): #one of the events
        actor = next(actor for actor in self.actors if actor.name==actorName)
        print '---------------------'
        print actor.cap_name,'has arrived!'
        print '---------------------'
        print
        actor.isHidden=False
        
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
            if len([actor for actor in self.actors if actor.team != self.currentActor.team and not actor.isDisabled and not actor.isHidden]) > 1: 
                legalOptions.append(allOptions[15]) #Focus
            legalOptions.append(allOptions[9]) #menu help
            legalOptions.append(allOptions[10]) #status
            legalOptions.append(allOptions[11]) #quit
        return legalOptions
    
    def setFocus(self):
        self.turnOver = False
        otherTeam = [actor for actor in self.actors if actor.team != self.currentActor.team and not actor.isDisabled and not actor.isHidden]
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
        #I feel like this sort of check could be built into a getFocus method
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
            turnText=turnText.replace("OFFENSE",self.currentActor.cap_name)
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
        self.roundCount=1
        turn = 100 #The game "counts down" from 100 and each actor gets a turn whenever their number comes up
        while not self.gameEnd(): #TODO: One weird thing is that gameEnd is run every tick of initiative
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
                    elif not actor.isHidden:
                        self.currentActor = actor #TODO: Should this just be a parameter?
                        self.takeTurn()
                        print
                        print
                        time.sleep(1)

            turn -= 1
            if turn == -100:
                self.roundCount+=1
                turn = 100


class Game:
    def __init__(self):
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        print '^^^^  UNLUCKY AT CARDS  ^^^^^'
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        print 
        player = self.loadPlayer()
        scenarioChoice = self.pickScenario()
        print
        scenario = Scenario(data.allScenarios[scenarioChoice], player)
        self.savePlayer(scenario.finalPlayer)

        
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

    def loadPlayer(self):
        try:
            f = file('test.uap','r')
            loadPlayer = pickle.load(f)
            f.close()   
            return loadPlayer     
        except:
            name = raw_input('What is your character\'s name? ')
            newPlayer = class_overall.Actor(name)
            newPlayer.addRoots()
            newPlayer.addWeapon(['six-shooter','shotgun','rifle','saber'])
            return newPlayer
        
    def savePlayer(self, player):
        f = file('test.uap','w')
        pickle.dump(player, f)
        f.close()




game = Game()


