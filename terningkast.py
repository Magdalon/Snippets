from random import randint

def terningkast():
    kast = int(input("Hvor mange terningkast?"))
    seksere = 0
    for i in range(kast):
        if randint(1,6) == 6:
            seksere +=1
    print("Antall seksere:")
    print(seksere)

terningkast()