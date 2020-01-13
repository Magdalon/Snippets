# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:49:01 2020

@author: magdalon
"""

from random import sample

import matplotlib.pyplot as plt
#import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

INSTILLINGER = {
        'startPredator': 10,
        'startPrey' : 100,
        'startmett':10,
        'mat' : 1000
        }

class Miljø(object):
    def __init__(self, nPredator = INSTILLINGER['startPredator'], nPrey = INSTILLINGER['startPrey']):
        self.populasjon = []
        [Prey(self) for i in range(nPrey)]
        [Predator(self) for i in range(nPredator)]
        self.hPrey = [self.nPrey()]
        self.hPredator = [self.nPredator()]
        
    def __str__(self):
        return str(self.populasjon)

    def __repr__(self):
        return str(self)
    
    def aktiver(self):
        aktive = self.populasjon
        for individ in aktive:
            individ.aktiver()           
        #self.plotHistorie()
        
    def iterer(self,T):
        for i in range(T):
            print("Iterasjon:",str(i+1),"Predatorer:", self.nPredator(),"Prey:",self.nPrey())
            self.aktiver()
            self.hPredator.append(self.nPredator())
            self.hPrey.append(self.nPrey())
        self.plotHistorie()
        
    def plotHistorie(self):
        plt.plot(self.hPredator, label="predator")
        plt.plot(self.hPrey, label= "prey")
        plt.legend()
        plt.show()

    def nPredator(self):
        return len([individ for individ in self.populasjon if type(individ) == Predator])
        
    def nPrey(self):
        return len([individ for individ in self.populasjon if type(individ) == Prey])

    def plotPP(self,burn = 0):
        plt.plot(jorden.hPredator[burn:],jorden.hPrey[burn:])
        plt.show()

    def plotPP3D(self,burn = 0):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(self.hPredator[burn:],self.hPrey[burn:],range(len(jorden.hPredator[burn:])))
        plt.show()
        
    
class Dyr(object):
    def __init__(self, verden, startmett = INSTILLINGER['startmett']):
        self.verden = verden
        self.mett = startmett
        self.verden.populasjon.append(self)
        
    def dø(self):
        self.verden.populasjon.remove(self)

    def former(self,partner):
        if(self.mett >1 and partner.mett >1):
            self.mett = self.mett/2
            partner.mett = partner.mett/2
            self.__class__(self.verden,self.mett)

    def aktiver(self):
        print("ERROR!")

class Predator(Dyr):
    def spis(self,bytte):
        self.mett += bytte.mett
        bytte.dø()
    
    def aktiver(self):
        self.mett -=1
        if self.mett <0:
            return self.dø()
        møte = sample(self.verden.populasjon,1)[0]
        #print(self,"møtte",møte)
        if type(self) == type(møte):
            self.former(møte)
        else:
            self.spis(møte)
            
class Prey(Dyr):
    def aktiver(self):
        self.mett = self.mett - 1 + INSTILLINGER['mat']/self.verden.nPrey()
        møte = sample(self.verden.populasjon,1)[0]
        #print(self,"møtte",møte)
        if type(self) == type(møte):
            self.former(møte)
       
jorden = Miljø()
jorden.iterer(10)