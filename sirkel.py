# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:49:55 2016

@author: magopda
"""

from math import pi
from math import pow

class Sirkel:
    def __init__(self,radius):
        self.radius=radius
    def omkrets(self):
        return 2*pi*self.radius
    def areal(self):
        return pi*(pow(self.radius,2))

r = int(input("Radius?\n"))

minSirkel = Sirkel(r)

print("Omkrets:")
print(minSirkel.omkrets())

print("Areal:")
print(minSirkel.areal())