from math import pi
from math import pow
class Kule:
    def __init__(self,radius):
        self.radius=radius
    def overflate(self):
        return 4*pi*(pow(self.radius,2))
    def volum(self):
        return 4*pi*(pow(self.radius,3))/3

r = int(input("Radius ?\n"))
    
minKule = Kule(r)

print("Overflate:")
print(round(minKule.overflate(),1))

print("Volum:")
print(round(minKule.volum(),1))