#a class for weapons.  simple for now, but expandable.

class Weapon:
    def __init__(self,name,range,maxbullets,sharp,isRange):
        self.name=name
        self.range=range #multiply this number by range addition in hit
        self.maxbullets=maxbullets
        self.bullets=maxbullets
        self.sharp=sharp #add to damage calculation
        self.isRange=isRange
     
    def __str__(self):
        return "Range penalty x"+str(self.range)+"Max bullets:"+str(self.maxbullets)+"Extra damage"+str(self.sharp)
    
    def reload(self):
        self.bullets = self.maxbullets

    def strRange(self):
        if not self.isRange:
            return 'Melee Range'
        if self.range == 0:
            return 'Short Range'
        if self.range == 1:
            return 'Medium Range'
        if self.range == 2:
            return 'Long Range'
    def strDamage(self):
        if self.sharp == 0:
            return 'Normal Damage'
        elif self.sharp <= 20:
            return 'High Damage'
        else:
            return 'Massive Damage'
        
        