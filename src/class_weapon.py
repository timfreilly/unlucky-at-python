#a class for weapons.  simple for now, but expandable.

from data import allWeapons

class WeaponType:
    _Types = dict()
    
    @classmethod
    def TypeFromName(cls, name):
        if name not in cls._Types:
            cls._Types[name] = cls(name)
        return cls._Types[name]

    def __init__(self,name): #,name,range,maxbullets,damage,isRange
        for weapon in allWeapons:
            if weapon['name'] == name:
                self.name=weapon['name']
                self.rangePenalty=weapon['range'] #multiply this number by range addition in hit EX (shotgun) 2 * 12ft = -24
                self.maxBullets=weapon['maxbullets']
                self.ammoName=weapon['ammo']
                self.isRange=weapon['isRange']
                self.flags=weapon['flags']
        
    def strRange(self):
        if not self.isRange:
            return 'Melee Range'
        if self.rangePenalty == 0:
            return 'Long Range'
        if self.rangePenalty == 1:
            return 'Medium Range'
        if self.rangePenalty == 2:
            return 'Short Range'
        
class Weapon:
    def __init__(self,name):
        self.type = WeaponType.TypeFromName(name)
        self.bullets = self.type.maxBullets  
        self.drawn = False
              
class Gear:
    def __init__(self):
        self.weapons = []
        self.ammos = []
        
    def addAmmo(self,type,quantity):
        for ammo in self.ammos:
            if ammo[0] == type:
                ammo[1] += quantity
                return
        self.ammos.append([type,quantity])
        
    def ammoCount(self,type):
        for ammo in self.ammos:
            if ammo[0] == type:
                return ammo[1]
        return 0
    
    def useAmmo(self,type,quantity):
        for ammo in self.ammos:
            if ammo[0] == type:
                ammo[1] -= quantity if ammo[1] >= quantity else 0
                