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
    liste = list(liste)
    liste.sort()
    if len(liste) == 0:
        return ""
    elif len(liste) == 1:
        return liste[0]
    else:
        return ", ".join(liste[:-1]) + " og " + liste[-1]


class Element:
    farge = FARGE["rød"]
    muligeHandlinger = ["undersøk", "slå", "løft"]
    def __init__(self, navn=None, sted = None, beskrivelse = None, funfacts = None, helse = 1, kommentarer = None, innhold = None, fokus = None):

        
        self.helse = helse
        
        self.sted = sted
        self.startsted = sted
        if sted:
            sted.innhold.append(self)
        
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

        if kommentarer:
            self.kommentarer = kommentarer
        else:
            self.kommentarer = {}       

        self.ødelagt = False
        self.ødelegger = None
 
        if funfacts:
            self.funfacts = funfacts
        else:
            self.funfacts = []
        
        if fokus:
            self.fokus = fokus
        else:
            self.fokus = None

    def handlinger(self):
        return "Mulige handlinger: " + FARGE["grønn"] + tekst(self.muligeHandlinger) +S

    def undersøk(self):
        return self.beskrivelse + ("\n"+sample(self.funfacts,1)[0] if self.funfacts else "")  + "\n" + self.handlinger() 

    def slå(self, person = None):
        self.helse -= 1
        if self.helse <0:
            return "Du slår " + self.navn + ". " + self.ødelegg()
        else:
            return "Du slår " + self.navn + ". " + (self.kommentarer["slå"] if "slå" in self.kommentarer.keys() else "")
    
    def ødelegg(self, person = None):
        svar = "Den går i stykker."
        self.helse = 0
        self.ødelegger = person
        self.navn = "Ødelagt " + self.navn
        self.beskrivelse = self.beskrivelse + ("Den ble ødelagt av "+person.navn +"." if self.ødelegger else "ingen vet hvem som ødela den.")
        return svar
    
    def løft(self):
        return self.pnavn() + " sitter fast eller er for tung til å løftes."
        
    def __str__(self):
        return self.pnavn() 

    def pnavn(self):
        return self.farge + self.navn+ ("" if self.helse else " (ødelagt)") + S
    
    def gåInn(self,sted):
        self.sted = sted
        sted.innhold.append(self)
        
    def gåUt(self,sted):
        self.sted = None
        sted.innhold.remove(self)
        

class Søl(Element):
    muligeHandlinger = Element.muligeHandlinger + ["tørk"]
    def tørk(self, person = None):
        return "Du har ingen ting å tørke med"
    
class Bokhylle(Element):

    def undersøk(self):
        if self.innhold:
            return ", ".join(self.innhold) + "\n" + self.handlinger()
        else:
            return "Bokhyllen er tom. Bøker er gammeldags, på BKV er vi på lag med framtiden!" + "\n" + self.handlinger()
        
    
class Kopimaskin(Element):
    def __init__(self, navn = None, papir=None,  toner=None, utskriftskø=None,**kwargs):
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

        super().__init__(navn,**kwargs)
        
    def undersøk(self):
        return "Dette er en kopimaskin" +  (". Noen har satt i gang en stor utskrift." if self.utskriftskø else ".") + "\n" +self.handlinger()
         
class Kaffetrakter(Element):
    pass




class Person(Element):
    farge = FARGE["blå"]
    
    def __init__(self, navn = False, sted = None, **kwargs):
        super().__init__(navn, **kwargs)
        standardfacts = ["Nei, hva skal man egentlig si om " + (navn if navn else "denne ukjente personen ?"),
                         "Det er ikke lov å undersøke kollegaer #metoo",
                         ]
        self.funfacts = self.funfacts + standardfacts
        if sted:
            self.gåInn(sted)
    def flytt(self, nyttSted):
        self.gåUt()
        self.gåInn(nyttSted)
        
    def gåUt(self):
        self.sted.personer.remove(self)
        self.sted = None
        
        
    def gåInn(self,rom):
        rom.personer.append(self)
        self.sted = rom
        self.fokus = rom
       
    def ødelegg(self,person=None):
        svar = "Du slo " + self.navn.upper() + " bevistløs!"
        self.ødelegger = person
        self.helse = 0
        self.navn = self.navn
        self.beskrivelse = self.beskrivelse + ("Hen ble slått bevistløs av "+person.navn +"." if self.ødelegger else "ingen vet hvem som drepte hen.")
        return svar

    def pnavn(self):
        return self.farge + self.navn+ ("" if self.helse else " (bevistløs)" ) + S


class Rom:
    def __init__(self, navn = "", beskrivelse = "", innhold = None):
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.naborom = {}
        self.personer = []
        if innhold:
            self.innhold = innhold
            for gjenstand in innhold:
                gjenstand.sted = self
        else:
            self.innhold = []
    
    def info(self):
        svar = [self.beskrivelse]
        if self.personer and len(self.personer)>1: 
            svar.append(tekst(map(str,self.personer)) + " er her.")
        if self.innhold:
            svar.append(tekst(map(str,self.innhold)) + " er her.")
        retninger = []
        for retning, rom in spiller.sted.naborom.items():
            retninger.append(FARGE["grønn" ] + retning + S+": " + rom.navn)
        svar.append("   ".join(retninger))
        return svar
    
    def __str__(self):
        return self.navn
     
    def handling(self, kommando, person):
        if kommando[0] in self.naborom.keys():
            person.flytt(self.naborom[kommando[0]])
            return True

        elif len(kommando)>1:
            for element in self.personer + self.innhold:
                if element.navn.lower() == kommando[1]:
                    person.fokus = element
                    return getattr(element,kommando[0])()
        else: 
            return getattr(person.fokus,kommando[0])()
      
        return False
               
    def leggTilNaborom(self, rom, himmelretning):
        self.naborom[himmelretning] = rom
        rom.naborom[motsattVei[himmelretning]] = self
   
    def undersøk(self, person = None):
        return "\n".join(self.info())
    
    def slå(self,person = None):
        return "Du slår i veggen. Ingen ting skjer"
    
    def løft(self,person = None):
        return "Det går ikke an"


class Utgang(Rom):
    def __init__(self, navn = "", beskrivelse = ""):
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.naborom = {}
        self.personer = []
       



mattekontor = Rom("mattekontoret",
                  "Dette er kontoret til mattelærerne.",
                  [Bokhylle(), Søl("kaffesøl")])
g1 = Rom("gangen", 
         "En helt vanlig gang, med kjedelige hvite vegger")
g1.leggTilNaborom(mattekontor,"s")
g2 = Rom("gangen", 
         "En helt vanlig gang, med kjedelige hvite vegger", 
         [Kopimaskin()])
g1.leggTilNaborom(g2,"ø")
toalett = Rom("toalettet",
              "Det er tre toaletter i denne kroken. Et for kvinner, et for menn, og et for de som ikke har bestemt seg.")
g2.leggTilNaborom(toalett,"n")
trappSør = Utgang("trapp")
trappSør.leggTilNaborom(g2,"n")

simenKontor = Rom("Simen sitt kontor", 
                  "Den kompetente og modige Simen har innredet dette lagerrommet til sitt eget kontor")
simenKontor.leggTilNaborom(g2,"v")

samfunnsfagkontor = Rom("samfunnsfagkontoret",
                        "Her sitter samfunnsfaglærerne")
samfunnsfagkontor.leggTilNaborom(g1,"ø")

g3 = Rom("gangen",
         "En helt vanlig gang, med kjedelige hvite vegger",[Bokhylle()])
g3.leggTilNaborom(g1,"s")

løveid = Rom("møterom Løveid",
             "Et helt vanlig møterom.")
løveid.leggTilNaborom(g3,"v")

g4 = Rom("gangen",
         "En helt vanlig gang, med kjedelige hvite vegger", 
         [Element("klesstativ")])
g4.leggTilNaborom(g3,"s")

personalrom=Rom("personalrommet", 
                "Dette er personalrommet. Her sitter lærerne når de ikke har noe bedre å bedrive tiden til", 
                [Kaffetrakter(),
                 Element("kjøleskap")])
personalrom.leggTilNaborom(g4,"ø")

norsklærerkontor = Rom("norsklærerkontoret", 
                       "Her sitter norsklærerne")
norsklærerkontor.leggTilNaborom(g4,"s")

g5 = Rom("gangen",
         "En helt vanlig gang, med kjedelige hvite vegger")
g5.leggTilNaborom(g4,"v")

trappNord = Utgang("trappen")
trappNord.leggTilNaborom(g5,"n")

heis = Rom("heisen")
heis.leggTilNaborom(g5,"v")


def kontroller(kommando, sted, person):
    pass

startsted = mattekontor
spiller = Person("Du",startsted)
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

steg = 0

print(FARGE["grønn"])
print('''
---------------------------
       TEKSTKRIGER
klarer du å komme deg hjem?
---------------------------''')
print(S)
print('''Advarsel: Alle likheter med virkelige steder, personer og hendelser er tilfeldige

''')
while(True):
    steg += 1
    print(FARGE["mangenta"] + "Du er på "+ str(spiller.sted)+S)
    if not type(spiller.fokus) == Rom:
        print("Du ser på " + spiller.fokus.pnavn())
    print(spiller.fokus.undersøk())
    kommando = input("Hva gjør du? (\"q\" for å avslutte, \"h\" for hjelp)\n")
    print()
    if kommando == "q":
        break
    elif kommando == "h":
        print("Skriv \"undersøk <navn på person eller gjenstand>\" for å undersøke det som er i rommet.")
        continue
    else:
       retur = spiller.sted.handling(kommando.lower().split(), spiller)
        
    if not retur:
       print("Det kan du ikke gjøre")
       print()
    
    if type(spiller.sted) == Utgang:
        print("Du fant utgangen etter " + str(steg)+ " steg. Gratulerer")
        break
    