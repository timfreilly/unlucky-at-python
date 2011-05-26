import random
import time
import math
import copy

#I like super testing

import class_weapon

locationAndDamage=[["Left Leg", 40, 70, 200, 1000], #allows for mods over 100, 4th slot has no value for lower body parts
                   ["Right Leg", 40, 70, 200, 1000],
                   ["Non-Gun Arm", 50, 90, 200, 1000],
                   ["Gun Arm", 30, 80, 200, 1000],
                   ["Left Shoulder", 40, 70, 90, 200],
                   ["Right Shoulder", 40, 70, 90, 200],
                   ["Gut",  30, 60, 80, 200],
                   ["Chest", 20, 70, 80, 200],
                   ["Head", 10, 40, 70, 100]]
    



class Actor:
    def __init__(self, chosenName, isNPC=False):
        self._name=chosenName
        self.brav=random.randint(1,100)
        self.conc=random.randint(1,100)
        self.grit=random.randint(1,100)
        self.losthp=0
        self.concuss=0         #negative up to 15
        self.morale=100
        self.healthRoot=0      #set to 7 if player picks that root
        self.concussionRoot=0  #set to 1 if player picks that root
        self.grappleActor=None #stores a player that is either grappling or grabbled by the actor
        self.x=0
        self.y=0
        self.team=''
        self.isNPC=isNPC
        self.flags=[]          #flags are temporary status effects that modify rolls
                               #current flags: MOVINGFAST, MOVINGSLOW, DRAWING, DIGGING
        self.focus=None        #focus is the actor whom this actor is currently "Locked On" to.
                               #It is meant to be used to get early 3+ support in, and may disappear after
        self.gear=class_weapon.Gear()
        
        
    def __str__(self):
        return self.cap_name+"'s stats: "+str(self.hp)+" Health Points, \nBravery: "+str(self.brav)+"\tConcentration: "+str(self.conc)+"\tGrit: "+str(self.grit)
    
    def showStatus(self): #might make more sense in Scenario
        print "Current stats for",self.name,":"
        print "Bravery: ",self.brav,"\tConcentration: ",self.conc,"\tGrit: ",self.grit
        print "Health Points: ",self.hp-self.losthp,"/",self.hp
        print "Wounds/Concussion Penalty: "+str(int(self.wounddebuff+self.concuss))+"%"
        print "Intimidation level: ",self.descIntimidation()
        print "Position X:",self.x,'Y:',self.y
    
    def get_name(self):
        return self._name
    def set_name(self,name):
        self._name = name
    name = property(get_name,set_name) #use name for middle of a sentence

    def get_cap_name(self):
        if self._name.find("the ")==0 or self._name.find("a ")==0 or self._name.find("an ")==0: #if the name starts with "the "
            return self._name.capitalize()
        else:
            return self._name
    cap_name = property(get_cap_name) #use cap_name for the start of a sentence
    
    def getMaxHP(self):
        return int(30+self.getBonus(self.grit)+self.healthRoot)
    hp = property(getMaxHP)
    
    def getIsDisabled(self):
        if self.losthp > .6 * self.hp:
            return True
        elif self.morale <= 25:
            return True
        elif self.concuss > .4 * self.hp:
            return True
        else:
            return False
    isDisabled = property(getIsDisabled)
    
    def getWoundDebuff(self):
        return -float(self.losthp)/self.hp * 40 #debuff is from -1 to -39
    wounddebuff = property(getWoundDebuff)

    def getMoveDebuff(self):
        if 'MOVINGSLOW' in self.flags:
            return -10
        elif 'MOVINGFAST' in self.flags:
            return -15
        else:
            return 0
    movedebuff = property(getMoveDebuff)
    
    def getDrawDebuff(self):
        if 'DRAWING' in self.flags:
            return -15
        else:
            return 0
    drawdebuff = property(getDrawDebuff)
    
    def getGrapplingBonus(self):
        if 'GRABBING' in self.flags:
            return 15
        else:
            return 0
    grapplingbonus = property(getGrapplingBonus)
    
    def getBonus(self,stat):
        return 3*math.floor((stat-40)/10)
    
    def clearBasicFlags(self):  #clears temporarily flags
        self.flags = [i for i in self.flags if i not in ('MOVINGFAST','MOVINGSLOW','DRAWING')] #uses list comprehension to remove the basic flags
        
    def breakGrapple(self):
        self.grappleActor.flags = [i for i in self.flags if i not in ('GRABBED','GRABBING')]
        self.grappleActor.grappleActor = None
        self.grappleActor = None
        self.flags = [i for i in self.flags if i not in ('GRABBED','GRABBING')]
    
    def rollDice(self,useDig=True):
        roll = random.randint(1,100)
        if useDig and 'DIGGING' in self.flags:
            print
            print self.cap_name,'summons extra strength...'
            time.sleep(2)
            roll += 20
            self.flags.remove('DIGGING')
        return roll

    def addRoots(self):
        if not self.isNPC:
            print "Select your Roots"
            print
        roots = 1 if (self.brav+self.conc+self.grit)>120 else 2
        if not self.isNPC and roots == 2:
            print "Due to your tough upbringing, pick two Roots."
            print
        while roots:
            roots -= 1
            if self.isNPC:
                root = random.randint(1,6)
            else:
                print "1. Troublemaker    +10 bravery        (connecting punches, grabs)"
                print "2. Wary eye        +10 concentration  (aiming guns)"
                print "3. Trail worn      +10 grit           (health, intimidation)"
                print "4. Lucky           +7  health         (lots of stamina)"
                print "5. Jack of spades  +20 lowest trait"
                print "6. Knuckles        +1  concussion     (harder punches)"
                root = 0
                while root not in range(1,7):
                    try:
                        root=input("Choose the number of your Root: ")
                    except SyntaxError:
                        print "Please enter your choice by number."
                    except NameError:
                        print "Please enter your choice by number."
                print
            if root==1:
                self.brav+=10
            elif root==2:
                self.conc+=10
            elif root==3:
                self.grit+=10
            elif root==4:
                self.healthRoot=7
            elif root==5:
                lowest = min(self.brav,self.conc,self.grit)
                if lowest == self.brav:
                    self.brav += 20
                elif lowest == self.conc:
                    self.conc += 20
                else:
                    self.grit += 20
            elif root==6:
                self.concussionRoot=1

    def addWeapon(self,weaponList):
        if self.isNPC:
            weaponChoice=random.randint(0,len(weaponList))
        else:
            weaponChoice = 0
            print "Choose your weapon:"
            for x,weap in enumerate(weaponList):
                type = class_weapon.WeaponType.TypeFromName(weap)
                if type.isRange:
                    print str(x+1)+'.',type.name.capitalize(),'\t',type.strRange(),'\t',type.maxBullets,type.ammoName
                else:
                    print str(x+1)+'.',type.name.capitalize(),'\t',type.strRange()
            while weaponChoice < 1 or weaponChoice > len(weaponList):
                try:
                    print
                    weaponChoice=input("Which weapon will you use?")
                except SyntaxError:
                    print "Please enter your choice by number."
                except NameError:
                    print "Please enter your choice by number."
        self.weapon = class_weapon.Weapon(weaponList[weaponChoice-1])
        self.gear.weapons.append(self.weapon)
        self.gear.addAmmo(self.weapon.type,self.weapon.type.maxBullets*3) #TODO: revert after debugging
        print self.cap_name,"chooses a",self.weapon.type.name+'.'
      
    def rangeChanceCalc(self,target):
        rangeChance=(50 + self.getBonus(self.conc) + self.drawdebuff + self.movedebuff + self.wounddebuff
                     +self.concuss + self.weapon.type.rangePenalty*self.distanceTo(target) + target.movedebuff)
        return rangeChance
    def meleeChanceCalc(self,target):
        meleeChance=(50 + self.getBonus(self.brav) + self.wounddebuff + self.concuss + self.grapplingbonus +
                     target.movedebuff) + self.drawdebuff
        return meleeChance

    def getDamage(self):
        locRoll=self.rollDice()
        if locRoll<=15:
            location=locationAndDamage[0]
        elif locRoll <=30:
            location=locationAndDamage[1]
        else :
            location=locationAndDamage[(locRoll-20)/10]
        
        roll=self.rollDice()
        if roll <=location[1]:
            damage=2
            depth="Scratch damage "
        elif roll <=location[2]:
            damage=4
            depth="Light wound "
        elif roll <=location[3]:
            damage=8
            depth="Serious wound "
        else:
            damage=12
            depth="Massive wound "
        print "Hit!   "+ depth+"to the "+location[0]+":",
        return damage

    def draw(self):
        self.weapon.drawn = True
        self.flags.append('DRAWING')
    def shoot(self,target):
        self.weapon.bullets -= 1
        roll=self.rollDice()
        if not self.weapon.drawn:
            self.draw()
        if roll<=self.rangeChanceCalc(target):
            damage=self.getDamage()
            print damage,'damage.'
            target.losthp+=damage
        else:
            print "Shot missed!"
    def reload(self):
        if self.gear.ammoCount(self.weapon.type) < self.weapon.type.maxBullets:
            self.weapon.bullets += self.gear.ammoCount(self.weapon.type)
            self.gear.useAmmo(self.weapon.type, self.weapon.type.maxBullets)
        else:
            self.weapon.bullets = self.weapon.type.maxBullets
            self.gear.useAmmo(self.weapon.type, self.weapon.type.maxBullets)
        if self.gear.ammoCount(self.weapon.type) == 0:
            print
            print '**** LAST RELOAD ****'
            print
    def swing(self,target):
        roll=self.rollDice()
        if not self.weapon.drawn:
            self.draw()
        if roll<=self.meleeChanceCalc(target):
            damage=self.getDamage()
            print damage,'damage.'
            target.losthp+=damage
        else:
            print "Swing missed!"
    def punch(self,target):
        roll=self.rollDice()
        if roll<=self.meleeChanceCalc(target):
            damage=self.getDamage()
            print damage/2,'damage and',(damage/2)+self.concussionRoot,'concussion.'
            target.losthp+=damage/2
            target.concuss-=(damage/2)+self.concussionRoot
        else:
            print "Missed!"
    def grab(self,target):
        roll=self.rollDice()
        if roll<=self.meleeChanceCalc(target):
            print "Grab succeeds! Future punches are more likely to hit."
            self.flags.append('GRABBING')
            target.flags.append('GRABBED')
            self.grappleActor = target
            target.grappleActor = self
        else:
            print "Grab missed!"
    def escape(self): 
        grabber = self.grappleActor
        best = max(self.brav,self.conc,self.grit)
        escapeChance = (50 + self.getBonus(best) + self.wounddebuff + self.concuss)
        roll=self.rollDice()
        if roll <= escapeChance:
            print self.cap_name,'breaks from',grabber.name+'\'s grab',
            self.breakGrapple()
        else:
            print self.cap_name,'fails to break free from',grabber.name+'\'s grab!'
        if roll <= escapeChance - 30: #extra high success
            if self.brav == best:
                print 'and takes a swing at',grabber.name+'\'s face!'
                time.sleep(2)
                print
                self.punch(grabber)
            elif self.conc == best:
                print 'and takes a step back!'
                time.sleep(2)
                print
                self.moveTowards(grabber,-2)
            else:
                print 'and goes for a reversal grab!'
                self.grab(grabber)
                time.sleep(2)
                print
        else:
            print
    def intimidate(self,target):
        if self.getBonus(self.grit)+random.randint(1,10)>self.getBonus(target.grit)+random.randint(1,10):
            print "Intimidate succeeds! 3 successes will win."
            target.morale-=25
        else:
            print "Intimidate fails."
            target.intimcount+=10 if target.morale < 90 else 0
        print "Overall intimidation score:"
        print self.cap_name,": ",self.descIntimidation(),"\t\t",target.cap_name,": ",target.descIntimidation()
    def descWounds(self):
        if self.wounddebuff <= -10:
            print self.cap_name," has lost ",self.losthp," health and is",
        if self.wounddebuff <= -30:
            print "massively wounded."
        elif self.wounddebuff <= -20:
            print "seriously wounded."  
        elif self.wounddebuff <= -10:
            print "slightly wounded."
    def descDisabled(self):  #describes why a character is disabled
        if self.losthp > .6 * self.hp:
            return 'severely injured'
        elif self.morale <= 25:
            return 'scared into submission'
        elif self.concuss > .4 * self.hp:
            return 'dizzy and slumped over'
    def descIntimidation(self):
        if self.morale > 75:
            return 'Unafraid'
        elif self.morale > 50:
            return 'Flinching'
        elif self.morale > 25:
            return 'Shaky'
        else:
            return 'Afraid'

    def moveTowards(self,target,speed):
        self.flags.append('MOVINGSLOW' if speed <= 4 else 'MOVINGFAST')
        
        if speed < 1: #moving backwards
            self.x += speed if self.x < target.x else -speed
            self.y += speed if self.y < target.y else -speed
            return
        if abs(self.x-target.x) <=speed: #run will bring them to the closest spot
            self.x = target.x + (1 if self.x > target.x else -1)
        else:
            self.x += speed if self.x < target.x else -speed
                
        if abs(self.y-target.y) <=speed: #run will bring them to the closest spot
            self.y = target.y + (1 if self.y > target.y else -1)
        else:
            self.y += speed if self.y < target.y else -speed
    def distanceTo(self,target): #D&D 4E geometry
        return max(abs(self.x-target.x),abs(self.y-target.y))
        