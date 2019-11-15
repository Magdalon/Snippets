# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 13:50:07 2019

@author: magopda
"""

from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

class Person:
    def __init__(self, navn,meninger = {}):
        self.navn = navn
        self.meninger = meninger
         
    def sammenlign(self,person):
        antallPåstander = 0.0
        samenfallendePåstander = 0.0
        for påstand, holdning in person.meninger.items():
            if påstand in self.meninger.keys():
                antallPåstander +=1
                if self.meninger[påstand] == holdning:
                    samenfallendePåstander += 1
        return samenfallendePåstander/antallPåstander
    
    def __repr__(self):
        return self.navn + ": " + str(self.meninger)
    
def prompt(påstand):
    svar = input(påstand+"? (ja/nei)")
    positiv = ['Ja','ja','Y','y','J','j']
    negativ = ['Nei','nei','N','n']
    while not (svar in positiv or svar in negativ):
        svar = input("Det du skrev inn ble ikke godtatt. Svar ja eller nei.")
    if svar in positiv:
        return True
    else:
        return False

class Valgomat:
    def __init__(self, påstander = [], politikere = []):
        self.påstander = påstander
        self.politikere = politikere
    
    def visMeninger(self):
        pprint(self.meninger)
        return self.meninger
    
    def visPolitikere(self):
        pprint(self.politikere)
        return self.politikere
       
    def leggTilPolitiker(self, navn, holdninger):
        person = Person(navn,dict(zip(self.påstander,holdninger)))
        self.politikere.append(person)
        return person
        
    def sammenligning(self, deltaker):
        print(deltaker.navn,"er:")
        likheter = []
        for person in self.politikere:
            likhet = deltaker.sammenlign(person)
            likheter.append(likhet)
            print(likhet*100,"% enig med", person.navn)
        return likheter
 
    def grafiskSammenligning(self,deltaker):
        y_pos = np.arange(len(self.politikere))
        likheter = [x*100 for x in self.sammenligning(deltaker)]
        plt.ylim((0,100))
        plt.bar(y_pos,likheter,align='center', alpha = 0.5)
        plt.xticks(y_pos, [x.navn for x in self.politikere])
        plt.ylabel('enighet (%)')
        plt.title('Så enig er du med de forskjellige politikerne')
        plt.show()
        return 0
    
    def kjør(self, grafisk = True, leggTil = False):
        meninger = {}
        print("Velkommen til Magdalons valgomat.")
        print("Hvor enig er du med dem som stiller til valg?")

        for påstand in self.påstander:
            meninger[påstand] = prompt(påstand)
        deltaker = Person("Du",meninger)
        if leggTil: self.politikere.append(deltaker)
        if grafisk:
            self.grafiskSammenligning(deltaker)
        else:
            self.sammenligning(deltaker)
        return deltaker
    
testValgomat = Valgomat(["Send dem hjem", "Nok er nok", "Kloden har fått feber", "Alle skal få"])
testValgomat.leggTilPolitiker("Nils", [True, True, False, False])
testValgomat.leggTilPolitiker("Kåre", [False, True, False, False])
testValgomat.leggTilPolitiker("Tore", [False, False, True, True])
testValgomat.leggTilPolitiker("Egil", [False, True, True, False])
testValgomat.kjør()
