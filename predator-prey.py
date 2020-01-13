# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:48:38 2020

@author: magopda
"""

from random import random
from random import sample
from pprint import pprint
from collections import defaultdict
import matplotlib.pyplot as plt

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

INSTILLINGER = {
        'xdim' : 100,
        'ydim' : 100,
        'startPredator' : 100,
        'startPrey' : 1000,
        'startMettPredator' : 20,
        'startMettPrey' : 10,
        'vx' : 10,
        'vy' : 10,
        'gressOverbefolkning' : 10,
        'gressMetthet' : 2
        }

class Verden(object):
    def __init__(self,xdim = INSTILLINGER['xdim'], ydim = INSTILLINGER['ydim'], startPredator = INSTILLINGER['startPredator'], startPrey = INSTILLINGER['startPrey']):
        self.xdim = xdim
        self.ydim = ydim
        self.posisjon = defaultdict(list)
        self.populasjon = []
        
        self.settOpp(startPredator,startPrey)
        self.hPrey = [self.nPrey()]
        self.hPredator = [self.nPredator()]
        
    def leggTilDyr(self,dyr):
        self.populasjon.append(dyr)

    def settOpp(self, nPredator = 5, nPrey =5):
        [Predator(self,startmett=2*INSTILLINGER['startMettPredator']*random()) for i in range(nPredator)]
        [Prey(self,startmett = 2*INSTILLINGER['startMettPrey']*random()) for i in range(nPrey)]
    
    def __str__(self):
        return str(self.populasjon)
    
    def __repr__(self):
        return str(self)
    
    def flytt(self):
        aktive = self.populasjon
        for individ in aktive:
            individ.flytt()           
        #self.plot()
        self.plotHistorie()
        

    def plot(self):
        xPredator= [individ.pos[0] for individ in self.populasjon if type(individ) == Predator]
        yPredator= [individ.pos[1] for individ in self.populasjon if type(individ) == Predator]

        xPrey= [individ.pos[0] for individ in self.populasjon if type(individ) == Prey]
        yPrey= [individ.pos[1] for individ in self.populasjon if type(individ) == Prey]
        
        plt.scatter(xPredator,yPredator,label="Predator")
        plt.scatter(xPrey,yPrey,label="Prey")
        #plt.legend()
        plt.show()
        
    def iterer(self,T):
        
        for i in range(T):
            print("Iterasjon:",str(i+1),"Predatorer:", self.nPredator(),"Prey:",self.nPrey())
            self.flytt()
            self.hPredator.append(self.nPredator())
            self.hPrey.append(self.nPrey())
        #print(self)
        

    def plotHistorie(self):
        plt.plot(self.hPredator, label="predator")
        plt.plot(self.hPrey, label= "prey")
        plt.legend()
        plt.show()

    def nPredator(self):
        return len([individ for individ in self.populasjon if type(individ) == Predator])
        
    def nPrey(self):
        return len([individ for individ in self.populasjon if type(individ) == Prey])

    def plotPP(self):
        plt.plot(jorden.hPredator,jorden.hPrey)
        plt.show()

    def plotPP3D(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(self.hPredator,self.hPrey,range(len(jorden.hPredator)))
        plt.show()
        
class Dyr(object):

    nDyr = 0

    def __init__(self, verden, startx=None, starty=None, startmett = 10,  vx = None, vy = None):

        type(self).nDyr += 1
        
        self.idDyr = self.nDyr
                     
        self.verden = verden

        if startx == None:
            x = random()*self.verden.xdim
        else:
            x = startx
            
        if starty == None:
            y = random()*self.verden.ydim
        else:
            y = starty

        self.pos = (int(round(x)),int(round(y)))
        
        if vx == None: vx = INSTILLINGER['vx']
        if vy == None: vy = INSTILLINGER['vy']
    
        self.vx = int(round(vx))
        self.vy = int(round(vy))
        
        self.mett = startmett
               
        verden.posisjon[self.pos].append(self)
        verden.populasjon.append(self)
        #print("Ny",self)

    def flytt(self):
        self.mett -= 1       
        
        if self.mett <0:
            return self.dø()
        
        gpos = self.pos

        tvx = int(round(self.vx*(2*random()-1)))
        tx = self.pos[0] + tvx
        if tx < 0:
            tx=-tvx-self.pos[0]
        elif tx > self.verden.xdim:
            tx = 2*self.verden.xdim-tvx-self.pos[0]
            
        tvy = int(round(self.vy*(2*random()-1)))
        ty = self.pos[0] + tvy
        if ty < 0:
            ty=-tvy-self.pos[0]
        elif ty > self.verden.xdim:
            ty = 2*self.verden.xdim-tvy-self.pos[0]
                        
        self.pos = (tx,ty)
        
        naboer = self.verden.posisjon[self.pos].copy()
        [self.møt(individ) for individ in naboer]
        
        self.verden.posisjon[gpos].remove(self)
        self.verden.posisjon[self.pos].append(self)

    def former(self,partner):
        if(self.mett >1 and partner.mett >1):
            
            self.mett = self.mett/2
            partner.mett = partner.mett/2
            #print("Hanky Panky:", self,"og",partner)
            self.__class__(self.verden,self.pos[0],self.pos[1],self.mett)
        
    def dø(self):
        self.verden.populasjon.remove(self)
        self.verden.posisjon[self.pos].remove(self)
        #print(self,"døde")
        return 0
    
    def møt(self, individ):
        if type(self) == type(individ):
            self.former(individ)

    def __str__(self):
        return type(self).__name__ + str(self.idDyr) + ": ["+str(self.mett)+"]"  + str(self.pos) + "("+ str(self.vx) + ","+str(self.vy)+")"
 
    def __repr__(self):
        return str(self)


class Predator(Dyr):
    
    def spis(self,bytte):
        self.mett += bytte.mett/2
        bytte.dø()
        #print(self,"spiste",bytte)
        
        
    def møt(self,individ):
        if type(individ) == Predator:
            self.former(individ)
        elif type(individ) == Prey:
            self.spis(individ)
            
    
class Prey(Dyr):
    
    def flytt(self):
        super().flytt()
        if(len(self.verden.posisjon[self.pos])<INSTILLINGER['gressOverbefolkning']):
            self.mett += INSTILLINGER['gressMetthet']
            

jorden=Verden()
pprint(jorden)
jorden.plot()
jorden.iterer(100)


