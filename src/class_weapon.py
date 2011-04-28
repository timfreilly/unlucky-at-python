#a class for weapons.  simple for now, but expandable.

#allWeapons = [['Six-shooter',1,6,"standard",0,True],
#              ['Shotgun',2,3,"standard",10,True],
#              ['Rifle',0,1,"standard",30,True],
#              ['Saber',0,10,"saber",20,False]]

class Weapon:
    def __init__(self,ownerName,range,maxbullets,c,d,isRange):
        self.owner=ownerName
        self.range=range #multiply this number by range addition in hit
        self.maxbullets=maxbullets
        self.bullets=maxbullets
        self.special=c #for special styles
        self.sharp=d #add to damage calculation
        self.isRange=isRange
     
    def __str__(self):
        return self.owner+"'s weapon: Range penalty x"+str(self.range)+"Max bullets:"+str(self.maxbullets)+"Extra damage"+str(self.sharp)
