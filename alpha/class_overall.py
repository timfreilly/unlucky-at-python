

import random
import time
import math


locationAndDamage=[["Left Leg", 40, 70, 200, 1000], #allows for mods over 100, 4th slot has no value for lower body parts
                   ["Right Leg", 40, 70, 200, 1000],
                   ["Non-Gun Arm", 50, 90, 200, 1000],
                   ["Gun Arm", 30, 80, 200, 1000],
                   ["Left Shoulder", 40, 70, 90, 200],
                   ["Right Shoulder", 40, 70, 90, 200],
                   ["Gut",  30, 60, 80, 200],
                   ["Chest", 20, 70, 80, 200],
                   ["Head", 10, 40, 70, 100]]




    
def getBonus(stat):
    bonus=3*math.floor((stat-40)/10)
    return bonus

def reRoll():
    roll=random.randint(1,100)
    return roll

def smartCaps(name):
    if name.find("the ")==0:  #if the name starts with "the "
        return name.capitalize()
    else:
        return name


class Actor:
    def __init__(self, chosenName):
        self.name=chosenName
        self.brav=random.randint(1,100)
        self.conc=random.randint(1,100)
        self.grit=random.randint(1,100)
        self.hp=(30+getBonus(self.grit))
        self.losthp=0
        self.draw=False
        self.drawdebuff=0   #negative on the turn you draw
        self.move=0         #negative number
        self.dig=0          #dig deep up to 20
        self.grapple=0      #positive 15 on the one that's grappled
        self.wound=0        #negative, based on lost/total hp
        self.concuss=0      #negative up to 15
        self.intimcount=0
        self.dist=8
        
    def __str__(self):
        return smartCaps(self.name)+"'s stats: "+str(self.hp)+" Health Points, \nBravery: "+str(self.brav)+"\tConcentration: "+str(self.conc)+"\tGrit: "+str(self.grit)
    def addRoots(self,root):
        if root==1:
            self.brav+=10
        elif root==2:
            self.conc+=10
        elif root==3:
            self.grit+=10
        else:
            print "Error text!"
    def rangeChanceCalc(self,defense,offweapon):
        rangeChance=50+getBonus(self.conc)+self.drawdebuff+self.move+self.dig+self.wound+self.concuss+offweapon.range*(self.dist+defense.dist)+defense.move
        return rangeChance
    def meleeChanceCalc(self,defense,offweapon):
        meleeChance=50+getBonus(self.brav)+self.dig+self.wound+self.concuss+defense.grapple+defense.move
        return meleeChance
    def getLocation(self,roll=999):
        if roll==999:
            roll=reRoll()
        if roll<=15:
            location=locationAndDamage[0]
        elif roll <=30:
            location=locationAndDamage[1]
        else :
            location=locationAndDamage[(roll-20)/10]
        return location
    def getDamage(self,location,isMelee,offweapon, roll=999): #Concussion(melee) is true, range false
        if roll ==999:
            roll=reRoll()+offweapon.sharp
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
        if isMelee==False:
            print damage,"damage."
        else:
            damage=damage/2
            print damage,"damage and ",damage,"concussion."
        return damage

    def shoot(self,defense,offweapon):
        roll=reRoll()
        if roll<=self.rangeChanceCalc(defense,offweapon):
            damage=self.getDamage(self.getLocation(),False,offweapon)
            defense.losthp+=damage
        else:
            print "Shot missed!"
    def punch(self,defense,offweapon):
        roll=reRoll()
        if roll<=self.meleeChanceCalc(defense,offweapon):
            damage=self.getDamage(self.getLocation(),True,offweapon)
            defense.losthp+=damage
            defense.concuss-=damage
        else:
            print "Missed!"
    def grab(self,defense,offweapon):
        roll=reRoll()
        if roll<=self.meleeChanceCalc(defense,offweapon):
            print "Grab succeeds! Future punches are more likely to hit."
            defense.grapple=15
        else:
            print "Grab missed!"
    def intimidate(self,defense):
        if getBonus(self.grit)+random.randint(1,10)+self.dig>getBonus(defense.grit)+random.randint(1,10):
            print "Intimidate succeeds! 3 successes will win."
            self.intimcount+=1
        else:
            print "Intimidate fails."
            self.intimcount-=1
        print "Overall intimidation score:"
        print smartCaps(self.name),": ",self.intimcount,"\t\t",defense.name,": ",defense.intimcount
    def getWounds(self):
        wounds=self.losthp/self.hp
        if wounds >=.25:
            print smartCaps(self.name)," has lost ",self.losthp," points of health and is at "
        if wounds >=.75:
            print "a massive disadvantage due to wounds."
            self.wound=-30
        elif wounds >=.50:
            print "a serious disadvantage due to wounds."
            self.wound=-20
        elif wounds>=.25:
            print "a slight disadvantage due to wounds."
            self.wound=-10
        else:
            pass

