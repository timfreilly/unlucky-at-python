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
        self.spareAmmo = self.bullets * 3 if self.bullets else None 
        
    def reload(self):
        if self.spareAmmo < self.type.maxBullets:
            self.bullets += self.spareAmmo
            self.spareAmmo = 0
        else:
            self.bullets = self.type.maxBullets
            self.spareAmmo -= self.type.maxBullets
        if self.spareAmmo == 0:
            print
            print '**** LAST RELOAD ****'
            print