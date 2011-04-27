import random
import time
import math


import class_overall
import class_weapon


def smartCaps(name):
    if name.find("the ")==0: #if the name starts with "the "
        return name.capitalize()
    else:
        return name

def rootsMenu():
        print "(1) Troublemaker: +10 bravery"
        print "(2) Wary eye: +10 concentration"
        print "(3) Tanned hide: +10 grit"
        root = 0
        while root != 1 and root != 2 and root != 3:
                try:
                        root=input("Choose the number of your Root: ")
                except SyntaxError:
                        print "Please enter your choice by number."
                except NameError:
                        print "Please enter your choice by number."
        return root

def weaponsMenu():
    weaponChoice = 0
    print "Choose your weapon:"
    print "1. Six-shooter \tMedium range penalty\tSix bullets/ reload \tStandard damage"
    print "2. Shotgun \tHigh range penalty \tThree bullets/ reload \tIncreased damage"
    print "3. Rifle \tNo range penalty \tOne bullet/ reload \tMassive damage"
    print "4. Saber \tUsable from 0 to 2 feet\tNo reload \tIncreased damage"
    while weaponChoice < 1 or weaponChoice > 4:
        try:
            weaponChoice=input("Which weapon will you use?")
        except SyntaxError:
            print "Please enter your choice by number."
        except NameError:
            print "Please enter your choice by number."
    return weaponChoice

def weaponChoose(name,weaponChoice):
    if weaponChoice==1:
        x=class_weapon.Weapon(name,1,6,"standard",0,True)
        print smartCaps(name)," chooses a six-shooter."
    elif weaponChoice==2:
        x=class_weapon.Weapon(name,2,3,"standard",10,True)
        print smartCaps(name)," chooses a shotgun."
    elif weaponChoice==3:
        x=class_weapon.Weapon(name,0,1,"standard",30,True)
        print smartCaps(name)," chooses a rifle."
    elif weaponChoice==4:
        x=class_weapon.Weapon(name,0,10,"saber",20,False)
        print smartCaps(name)," chooses a saber."
    return x
    

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

def getLegalOptions(offense,defense,offweapon):
    legalOptions=[]
    dist=max(abs(offense.x-defense.y),abs(offense.x-defense.y))
    if dist>4:
        legalOptions=[allOptions[0]] #run    #TODO: hey yeah
    if dist>0: #TODO: Hey does fixme show up
        legalOptions.append(allOptions[1]) #walk
    if dist==0:
        legalOptions=[allOptions[2]] #punch
    if dist==0 and defense.grapple==0:
        legalOptions.append(allOptions[3]) #grab
    if defense.grapple==0 and offense.grapple==0:
        legalOptions.append(allOptions[12]) #back away
    if offweapon.type==True:
        if offweapon.bullets==0:
            legalOptions.append(allOptions[13]) #reload
        elif offense.draw==False:
            legalOptions.append(allOptions[4]) #draw and fire
            legalOptions.append(allOptions[5]) #draw and dig
        else:
            legalOptions.append(allOptions[6]) #fire
    if dist<=2 and offweapon.special=="saber":
        legalOptions.append(allOptions[14]) #saberize   
    legalOptions.append(allOptions[7]) #intimidate
    if offense.dig<=10:
        legalOptions.append(allOptions[8]) #dig deep
    if offense.name!="the banker":
        legalOptions.append(allOptions[9]) #menu help
        legalOptions.append(allOptions[10]) #status
        legalOptions.append(allOptions[11]) #quit
    return legalOptions



def menuChoice(offense,defense,offweapon):

    dist=max(abs(offense.x-defense.y),abs(offense.x-defense.y))
    legalOptions=getLegalOptions(offense,defense,offweapon)
    if offense.name=="the banker":
        print "The banker takes a turn.",
        count=0
        while count<=3:
            print ".",
            time.sleep(.5)
            count+=1
        print
        turnChoice=random.randint(1,len(legalOptions))
        print 
    else: # Prints a menu of legal options on the player's turn
        print "You are ",dist," feet from the banker."
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
    turnText=turnText.replace("OFFENSE",smartCaps(offense.name))
    turnText=turnText.replace("DEFENSE",defense.name)
    turnText=turnText.replace("DISTANCE",str(dist))
    turnText=turnText.replace("HALF",str(dist/2))
    print turnText
    turnAction=legalOptions[turnChoice-1][2] #Takes the action based on the choice
    if turnAction=="RUN": #fix for coordinates
        if dist<=8:
            offense.dist=0
            defense.dist=0 
        else:
            offense.dist=offense.dist-4
            defense.dist=defense.dist-4 
        offense.move=-20
        return 1
    elif turnAction=="WALK": #fix for coordinates
        if dist<=4:
            offense.dist=0
            defense.dist=0
        else:
            offense.dist=offense.dist-2
            defense.dist=defense.dist-2
        offense.move=-10
        return 1
    elif turnAction=="BACKAWAY": #fix for coordinates
        offense.dist=offense.dist+1
        defense.dist=defense.dist+1
        offense.move=-5
    elif turnAction=="PUNCH":
        offense.punch(defense,offweapon)
        offense.dig=0
        return 1
    elif turnAction=="GRAB":
        offense.grab(defense,offweapon)
        offense.dig=0
        return 1
    elif turnAction=="RELOAD":
        offweapon.bullets=offweapon.maxbullets
        return 1
    elif turnAction=="DRAWFIRE":
        offense.draw=True
        offense.drawdebuff=-10
        offense.shoot(defense,offweapon)
        offense.dig=0
        offweapon.bullets-=1
        return 1
    elif turnAction=="DRAWDIG":
        offense.draw=True
        offense.dig+=5
        return 1
    elif turnAction=="FIRE":
        offense.shoot(defense,offweapon)
        offense.dig=0
        offweapon.bullets-=1
        return 1
    elif turnAction=="SABER":
        offense.punch(defense,offweapon)
        offense.dig=0
    elif turnAction=="INTIM":
        offense.intimidate(defense)
        offense.dig=0
        return 1
    elif turnAction=="DIG":
        offense.dig+=10
        return 1
    
    elif turnAction=="MENU":
        print "A high Bravery means better punches, but you must be 0 distance away."
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
        print "Current stats for",offense.name,":"
        print "Bravery: ",offense.brav,"\t\tConcentration: ",offense.conc,"\t\tGrit: ",offense.grit
        print "Total Health Points: ",offense.hp,"\t\tLost Health Points: ",offense.losthp
        print "Buff from Dig Deep: ", offense.dig,"\t\tIntimidation success: ",offense.intimcount
        print "Debuff from wounds: ",offense.wound,"\t\tDebuff from concussion: ",offense.concuss
        print
        print "Current stats for",defense.name,":"
        print "Bravery: ",defense.brav,"\t\tConcentration: ",defense.conc,"\t\tGrit: ",defense.grit
        print "Total Health Points: ",defense.hp,"\t\tLost Health Points: ",defense.losthp
        print "Buff from Dig Deep: ", defense.dig,"\t\tIntimidation success: ",defense.intimcount
        print "Debuff from wounds: ",defense.wound,"\t\tDebuff from concussion: ",defense.concuss
        print
        time.sleep(2)
        return 0
    elif turnAction=="QUIT":
        return 2

def errorCatch(offense,defense, offweapon):
    successfulChoice=0
    while successfulChoice==0: #errors return 0, successes return 1
        successfulChoice=menuChoice(offense,defense,offweapon)
    if successfulChoice==2:
        return True  #return this value to quitChoice
    else:
        return False
   

def gameEnd(offense,defense):
    print
    print
    if defense.wound<=-20:
        print "The banker has sustained serious wounds and can't stop you from \n grabbing the cash.  You win!"
        return True
    elif offense.intimcount==3:
        print "You've intimidated the banker into subimssion and make off with the cash!"
        return True
    elif defense.concuss<=-15:
        print "The banker has sustained a concussion and sinks to the floor. You reach over him and grab the cash!"
        return True
    elif defense.intimcount==3:
        print "The banker is far too intimidating and will never back down.  You lose!"
        return True
    elif offense.wound<=-20:
        print "You have sustained serious wounds.  You lose!"
        return True
    elif turnCount>10:
        print "You've waited too long and the sheriff walks in the door.  You lose!"
        return True
    elif quitChoice==True:
        return True
    else:
        return False
    
    
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




#Character creation and choice of roots

player=class_overall.Actor(raw_input("What is your character's name?"))
player.x = 16
player.y = 16
print player
print
print "A Root improves one of your stats.  Bravery improves"
print "punches, Concentration improves shooting, and Grit improves"
print "intimidation."
print
if (player.brav+player.conc+player.grit)>120:
    player.addRoots(rootsMenu())
else:
    print "Total stats are under 120.  Choose two Roots."
    player.addRoots(rootsMenu())
    player.addRoots(rootsMenu())
print player
print
playerWeapon=weaponChoose(player.name,weaponsMenu())
#print playerWeapon

print
print "Creating stats for the banker."
time.sleep(1)
banker=class_overall.Actor("the banker")
banker.x = 0
banker.y = 0
if (banker.brav+banker.conc+banker.grit)>120:
    banker.addRoots(random.randint(1,3))
    print "The banker added one Root."
else:
    banker.addRoots(random.randint(1,3))
    banker.addRoots(random.randint(1,3))
    print "The banker added two Roots."
print banker
print
bankerWeaponChoice=random.randint(1,4)
bankerWeapon=weaponChoose(banker.name,bankerWeaponChoice)
#print bankerWeapon
time.sleep(1)

quitChoice=False
turnCount=1
while gameEnd(player,banker)==False:
    print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
    print "Beginning turn number ",turnCount,"."
    print "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~"
    time.sleep(1)
    quitChoice=errorCatch(player,banker,playerWeapon)  #player turn
 
    
    print
    turnCount+=1

    banker.getWounds()
    if gameEnd(player,banker)==True:  #checks for game end before banker turn
        print
        print "Goodbye!"
        break

    menuChoice(banker,player,bankerWeapon) #banker turn
    
    time.sleep(1)

    print
    player.getWounds()