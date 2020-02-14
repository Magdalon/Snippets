# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:50:03 2020

@author: magopda
"""

FARGE = {
        "svart": "\u001b[30m",
        "rød": "\u001b[31m",
        "grønn": "\u001b[32m",
        "gul": "\u001b[33m",
        "blå": "\u001b[34m",
        "mangenta": "\u001b[35m",
        "cyan": "\u001b[36m",
}

S = FARGE["svart"]

from random import sample
from random import random 

motsattVei = {"n":"s","s":"n","ø":"v","v":"ø","h":None}

def tekst(liste):
    if len(liste) == 0:
        return ""
    elif len(liste) == 1:
        return liste[0]
    else:
        return ", ".join(liste[:-1]) + " og " + liste[-1]


class Element:
    farge = FARGE["rød"]
    muligeHandlinger = ["undersøk", "slå", "løft"]
    def __init__(self, navn=None, beskrivelse = None, plassering = None, helse = 1, kommentarer = None, innhold = None):
        if navn:
            self.navn = navn
        else:
            self.navn = type(self).__name__.lower()
        if beskrivelse:
            self.beskrivelse = beskrivelse
        else:
            self.beskrivelse = "Dette er en " + self.pnavn() + "."
        if kommentarer:
            self.kommentarer = kommentarer
        else:
            self.kommentarer = {}
        
        if innhold:
            self.innhold = innhold
        else:
            self.innhold = []
        
        self.helse = helse
        self.ødelegger = None
        

    def handlinger(self):
        return "Mulige handlinger: " + FARGE["grønn"] + tekst(self.muligeHandlinger) +S

    def undersøk(self):
        return self.beskrivelse + "\n" + self.handlinger()

    def slå(self, person = None):
        self.helse -= 1
        if self.helse <0:
            return "Du slår " + self.navn + ". " + self.ødelegg()
        else:
            return "Du slår " + self.navn + ". " + (self.kommentarer["slå"] if "slå" in self.kommentarer.keys() else "")
    
    def ødelegg(self, person = None):
        svar = "Den går i stykker."
        self.ødelegger = person
        self.navn = "Ødelagt " + self.navn
        self.beskrivelse = self.beskrivelse + ("Den ble ødelagt av "+person.navn +"." if self.ødelegger else "ingen vet hvem som ødela den.")
        return svar
    def løft(self):
        return self.pnavn() + " sitter fast eller er for tung til å løftes."
        
    def __str__(self):
        return self.pnavn() 

    def pnavn(self):
        return self.farge + self.navn+ S

class Søl(Element):
    muligeHandlinger = Element.muligeHandlinger + ["tørk"]
    def tørk(self, person = None):
        return "Du har ingen ting å tørke med"
    
class Bokhylle(Element):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
    
    def handling(self,kommando,Person,rom):
        self.kommandoer

    def undersøk(self):
        if self.innhold:
            return ", ".join(self.innhold) + "\n" + self.handlinger()
        else:
            return "Bokhyllen er tom. Bøker er gammeldags, på BKV er vi på lag med framtiden!" + "\n" + self.handlinger()
        
    
class Kopimaskin(Element):
    def __init__(self, papir=None,  toner=None, utskriftskø=None):
        if papir:
            self.papir = papir
        else:
            papir = round(random()*2000)

        if toner:
            self.toner = toner
        else:
            self.toner = random()

        if utskriftskø:
            self.uskriftskø = utskriftskø
        else:
            self.utskriftskø = sample([True,False],1)[0]
        self.navn = type(self).__name__.lower()
        
    def undersøk(self):
        return "Dette er en kopimaskin" +  (". Noen har satt i gang en stor utskrift." if self.utskriftskø else ".") + "\n" +self.handlinger()
         
class Kaffetrakter(Element):
    pass


class Rom:
    def __init__(self, navn = "", beskrivelse = "", gjenstander = None):
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.naborom = {}
        self.personer = []
        if gjenstander:
            self.gjenstander = gjenstander
            for gjenstand in gjenstander:
                gjenstand.plassering = self
        else:
            self.gjenstander = []
        
    def __str__(self):
        return self.navn + "\n" + self.beskrivelse + "\n" + ", ".join(map(str,self.personer)) + " er her."
    
    def handling(self, kommando, Person):
        if kommando[0] in self.naborom.keys():
            return Person.flytt(self.naborom[kommando[0]])

        elif len(kommando)>1:
            for element in self.personer + self.gjenstander:
                if element.navn.lower() == kommando[1]:
                    return getattr(element,kommando[0])()
                    
        return False
               
    def leggTilNaborom(self, rom, himmelretning):
        self.naborom[himmelretning] = rom
        rom.naborom[motsattVei[himmelretning]] = self

    def gåInn(self,person):
        self.personer.append(person)
        return self.navn + "\n" + self.beskrivelse
    
    def gåUt(self, person):
        self.personer.remove(person)
        return ""

class Person(Element):
    farge = FARGE["blå"]
    def __init__(self, navn = "", sted = None, beskrivelse = "", funfacts = None,sekk =None, helse = 1, kommentarer = None,**kwars):
        self.navn = navn
        if sekk:
            self.sekk = sekk
        else:
            self.sekk = []
        self.sted = sted
        if sted:
            self.sted.gåInn(self)
        
        self.beskrivelse = beskrivelse
        
        standardfacts = ["Nei, hva skal man egentlig si om " + self.navn + "?",
                    "Det er ikke lov å undersøke kollegaer #metoo",
                    ]
        if funfacts:
            self.funfacts = standardfacts + funfacts
        else:
            self.funfacts = standardfacts
        self.helse = helse
        if kommentarer:
            self.kommentarer = kommentarer
        else:
            self.kommentarer = {}
            
        super().__init__(**kwargs)
        
    def flytt(self, nyttSted):
        gammeltSted = self.sted
        self.sted = nyttSted
        return gammeltSted.gåUt(self) + nyttSted.gåInn(self)

    def undersøk(self):
        return self.beskrivelse + sample(self.funfacts,1)[0]   + "\n" + self.handlinger() 

    def gåInn(self,rom):
        self.sted =rom
        return rom.gåInn(self)
       
    def ødelegg(self,person=None):
        svar = "Han dør. DU DREPTE " + self.navn.upper() + "!"
        self.ødelegger = person
        self.navn = "Død " + self.navn
        self.beskrivelse = self.beskrivelse + ("Hen ble drept av "+person.navn +"." if self.ødelegger else "ingen vet hvem som drepte hen.")
        return svar

class Utgang(Rom):
    def __init__(self, navn = "", beskrivelse = ""):
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.naborom = {}
        self.personer = []
       



mattekontor = Rom("Mattekontor",
                  "Dette er kontoret til mattelærerne.",
                  [Bokhylle(), Søl("kaffesøl")])
g1 = Rom("Gang", 
         "En helt vanlig gang, med kjedelige hvite vegger")
g1.leggTilNaborom(mattekontor,"s")
g2 = Rom("Gang", 
         "En helt vanlig gang, med kjedelige hvite vegger", 
         [Kopimaskin()])
g1.leggTilNaborom(g2,"ø")
toalett = Rom("Toalett",
              "Det er tre toaletter i denne kroken. Et for kvinner, et for menn, og et for de som ikke har bestemt seg.")
g2.leggTilNaborom(toalett,"n")
trappSør = Utgang("Trapp")
trappSør.leggTilNaborom(g2,"n")

simenKontor = Rom("Simen sitt kontor", 
                  "Den kompetente og modige Simen har innredet dette lagerrommet til sitt eget kontor")
simenKontor.leggTilNaborom(g2,"v")

samfunnsfagkontor = Rom("Samfunnsfagkontor",
                        "Her sitter samfunnsfaglærerne")
samfunnsfagkontor.leggTilNaborom(g1,"ø")

g3 = Rom("Gang",
         "En helt vanlig gang, med kjedelige hvite vegger",[Bokhylle()])
g3.leggTilNaborom(g1,"s")

løveid = Rom("Møterom løveid",
             "Et helt vanlig møterom.")
løveid.leggTilNaborom(g3,"v")

g4 = Rom("Gang",
         "En helt vanlig gang, med kjedelige hvite vegger", 
         [Element("klesstativ")])
g4.leggTilNaborom(g3,"s")

personalrom=Rom("Personalrom", 
                "Dette er personalrommet. Her sitter lærerne når de ikke har noe bedre å bedrive tiden til", 
                [Kaffetrakter(),
                 Element("kjøleskap")])
personalrom.leggTilNaborom(g4,"ø")

norsklærerkontor = Rom("Norsklærerkontoret", 
                       "Her sitter norsklærerne")
norsklærerkontor.leggTilNaborom(g4,"s")

g5 = Rom("Gang",
         "En helt vanlig gang, med kjedelige hvite vegger")
g5.leggTilNaborom(g4,"v")

trappNord = Utgang("Trapp")
trappNord.leggTilNaborom(g5,"n")

heis = Rom("Heis")
heis.leggTilNaborom(g5,"v")


def kontroller(kommando, sted, person):
    pass


spiller = Person("Du",False)
ikkespillere = [
        Person("Martin",
               mattekontor,
               funfacts = [
                       "Martin ser skeptisk på deg",
                       "Martin forteller deg en anekdote om Britisk politikk"
                       ],
               kommentarer = {"slå" : "Martin sier: \"Dette blir en personalsak\""}
               ),
        Person("Simen", simenKontor,
               funfacts = [
                       "Simen sier: Hvorfor gjør du slike ting?"
                       ]
               ),
        Person("Henrik",
               samfunnsfagkontor,
               funfacts = [
                       "Henrik liker Metal", 
                       "Henrik har på seg Metal t-skjorte",
                       "Henrik sier \"Do it!\""
                       ],
               kommentarer = {"slå" : "Henrik sier: \"Hold opp!\""}
               ),
        Person("Magdalon",
               mattekontor,
               funfacts = [
                       "Magdalon viser deg sitt siste prosjekt"]),
        Person("Kenny",
               mattekontor)
        ]

startsted = mattekontor

steg = 0

print(
'''
---------------------------
       TEKSTKRIGER
klarer du å komme deg hjem?
---------------------------

'''

      )



print(spiller.gåInn(mattekontor))
while(True):
    steg += 1
    if len(spiller.sted.personer) >0:
        print(tekst(list(map(str,spiller.sted.personer))) + " er her.")
    if len(spiller.sted.gjenstander) >0:
        print(tekst(list(map(str,spiller.sted.gjenstander))) + " er her.")
    if len(spiller.sted.personer) >0 or len(spiller.sted.personer) >0:
        print("Skriv \"undersøk <navn på person eller gjenstand>\" for å undersøke det som er i rommet")
    for retning, rom in spiller.sted.naborom.items():
        print(FARGE["grønn" ] + retning + S+": " + rom.navn ,end ="   ")
    print()
    kommando = input("Hva gjør du? (\"q \" for å avslutte) ")
    print()
    if kommando == "q":
        break
    else:
       retur = spiller.sted.handling(kommando.lower().split(), spiller)
       if retur:
          if type(retur) != bool:
              print(retur)
       else:
           print("Det kan du ikke gjøre")

    print()
    
    if type(spiller.sted) == Utgang:
        print("Du fant utgangen etter " + str(steg)+ " steg. Gratulerer")
        break
    