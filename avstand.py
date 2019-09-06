# -*- coding: utf-8 -*-

"""
Created on Thu Jun 20 21:10:38 2019

@author: magopda
"""

print("""Program som regner ut storsirkelavstanden mellom to punkter på overflaten til en planet.

Som et blatant eksempel på antrosentrisme er jorden tatt med som et standardeksempel.

  Funksjoner:
    visSteder()
      Liste over steder som er lagt til
  
    avstand( fra, til)
      Avstanden mellom to steder på jordkloden
    
    leggTilSted( navn, breddegrad, lengdegrad)
      Legger til et nytt sted på jordkloden
      
      breddegrad og lengdegrad kan være:
        desimaltall, med positiv retning for nord og øst
          for eksempel: jorden.leggTilSted("New York",40.75,-74)
      ELLER:
        et tuppel med fire elementer (grader, minutter, sekunder, himmelretning)

""")

# importerer nødvendige matematikkfunksjoner
from math import radians, cos, acos, sin

class Planet:
    def __init__(self,navn,diameter):
        self.navn=navn
        self.radius=diameter/2
        self.steder = {}

    def avstand(self,fra,til):
        return self.steder[fra].avstandTil(self.steder[til])
    
    def visSteder(self):
        return list(self.steder.values())

    def __repr__(self):
        return self.navn + ": Radius: " + str(self.radius) + "m , Steder: " + str(len(self.steder))
    
class Sted:
    def __init__(self,navn,breddegrad,lengdegrad,planet):
        self.navn= navn
        self.breddegrad = breddegrad 
        self.lengdegrad= lengdegrad
        self.planet = planet
        self.planet.steder[navn]=self
        
    def avstandTil(self,slutt,høyde=0):
        a= radians(90-self.breddegrad)
        b= radians(90-slutt.breddegrad)
        C= radians(self.lengdegrad - slutt.lengdegrad)
        c= acos(cos(a)*cos(b)+sin(a)*sin(b)*cos(C))
        return c * (self.planet.radius + høyde)

    def __repr__(self):
        return self.navn + "(" + str(round(self.breddegrad,2)) + "," + str(round(self.lengdegrad,2))+")"
        
# Lager en planet:
jorden = Planet("jorden",12742000)

# lager et brukergrensesnitt
# funksjon for å vise stedene som er lagt inn
def visSteder(planet=jorden):
    print("\n".join(map(str,planet.visSteder())))

# funksjon for å regne ut avstanden mellom to steder
def avstand(fra,til,planet = jorden):
    print("Avstanden fra",fra,"til",til,"er",round(planet.avstand(fra,til)/1000,0),"km i luftlinje")

# Definerer positive og negative himmelretninger i desimalgrader.
N=E=Ø=1
S=W=V=-1
# Funksjon som regner om fra grader, minutter og sekunder til desimalgrader
def gmsTilG(pos):   
    g,m,s,r=pos
    t = g
    t += m/60
    t += s/3600
    return r*t
    
# funksjon for å legge til sted
def leggTilSted(navn,breddegrad,lengdegrad,planet=jorden):
    if breddegrad.__class__==tuple:breddegrad = gmsTilG(breddegrad)
    if lengdegrad.__class__==tuple: lengdegrad = gmsTilG(lengdegrad)
    Sted(navn,breddegrad,lengdegrad,planet)
    print(jorden.steder[navn],"er lagt til.")
    
# Legger til noen steder.
leggTilSted("Bergen",(60,23,33,N),(5,19,24,Ø))
leggTilSted("Oslo",(59,54,40,N),(10,44,00,Ø))
leggTilSted("Bangkok",13,100)
leggTilSted("Amsterdam",54,4)
leggTilSted("New York",40.75,-74)
leggTilSted("Nordpolen",90,0)
leggTilSted("Sørpolen",-90,0)