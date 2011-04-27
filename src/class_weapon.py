#a class for weapons.  simple for now, but expandable.

class Weapon:
    def __init__(self,ownerName,a,b,c,d,isRange):
        self.owner=ownerName
        self.range=a #multiply this number by range addition in hit
        self.maxbullets=b
        self.bullets=b
        self.special=c #for special styles
        self.sharp=d #add to damage calculation
        self.type=isRange
     
    def __str__(self):
        return self.owner+"'s weapon: Range penalty x"+str(self.range)+"Max bullets:"+str(self.maxbullets)+"Extra damage"+str(self.sharp)
