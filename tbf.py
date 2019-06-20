# laster inn funksjonen shuffle, som vi skal bruke til � stokke om ordene
from random import shuffle

# funksjon som lager en liste over alle trebokstavsforkortelsene
def genererTbf():
    #lager en liste over alle bokstavene vi kan bruke
    bokstaver = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","æ","�","�"]
    # lager en tom liste som vi skal fylle med ord    
    ordliste = []
    # g�r gjennom bokstav-listen og plukker ut den f�rste bokstaven. Denne blir lagret som b1
    for b1 in bokstaver:
        # g�r gjennom bokstavlisten og plukker ut den andre bokstaven og lagrer den som b2
        for b2 in bokstaver:
            # g�r gjennom bokstavlisten og plukker ut den tredje bokstaven
            for b3 in bokstaver:
                '''
                legger sammen den f�rste, andre og tredje bokstaven
                bokstavene er av datatypen String, slik at n�r vi bruker + -tegnet
                sier vi at de skal settes etter hverandre.
                ordliste.append() betyr at vi skal legge det nye ordet til den nye ordlisten
                '''
                ordliste.append(b1+b2+b3)
    # returnerer den nye ordlisten
    return ordliste

# kaller FUNKSJONEN genererTfb og lagrer resultatet som VARIABELEN ordliste
ordliste = genererTbf()

# stokker om p� rekkef�lgen p� ordene i ordlisten
shuffle(ordliste)

# Skriver ut ordene i ordlisten, en og en
for o in ordliste: 
    print(o, end=" ")
    # print() er utskriftskommandoen til python. 