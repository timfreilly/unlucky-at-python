import random
import time
import copy
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
            ["Fire your WEAPON.",                       "OFFENSE attempts to shoot DEFENSE.",           "FIRE"] ,  
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
    def __init__(self, title, actors, teams, duration, timeOverMessage, introduction):
        self.title = title
        self.actors = actors
        self.teams = teams
        self.duration = duration
        self.timeOverMessage= timeOverMessage
        self.introduction = introduction
   
        

class Battle:
    def __init__(self,scenarioChoice):
        self.actors = []
        self.scenario = Scenario(**data.allScenarios[scenarioChoice])
        print self.scenario.introduction
        for partialActor in self.scenario.actors:
            self.createActor(partialActor)
    
    def getMembersOfTeam(self,team):
        members = []
        for member in self.actors:
            if member.team == team:
                members.append(member)
        return members
    
    def getMembersNotInTeam(self,team):
        members = []
        for member in self.actors:
            if member.team != team:
                members.append(member)
        return members
    
    def createActor(self,partialActor):
        print
        if partialActor['isNPC']:
            name = partialActor['name']
            print 'Creating',name
            time.sleep(1)
        else:
            name = raw_input('What is your character\'s name?')
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
        print
        print

        for team in self.scenario.teams:
            teamDisabled = True
            for actor in self.getMembersOfTeam(team['name']):
                if not actor.isDisabled:
                    teamDisabled = False
            if teamDisabled:
                print team['defeatMessage']
                return True

        if self.roundCount > self.scenario.duration:
            print self.scenario.timeOverMessage
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
                if self.currentActor.weapon.spareAmmo:
                    legalOptions.append(allOptions[13]) #reload
            elif self.currentActor.weapon.drawn==False:
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
            if len(self.getMembersNotInTeam(self.currentActor.team)) > 1: #allow focus switching, this check does not check if npcs are disabled
                legalOptions.append(allOptions[15])
            legalOptions.append(allOptions[9]) #menu help
            legalOptions.append(allOptions[10]) #status
            legalOptions.append(allOptions[11]) #quit
        return legalOptions
    
    def setFocus(self):
        otherTeam = self.getMembersNotInTeam(self.currentActor.team)
        if self.currentActor.isNPC:
            self.currentActor.focus = random.choice(otherTeam)
        else:
            if len(otherTeam)==1:
                self.currentActor.focus = otherTeam[0]
            else:
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
                self.currentActor.draw()
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

    def startBattle(self):
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
                    print self.currentActor.cap_name,'is',self.currentActor.descDisabled(),'and can not act!'
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