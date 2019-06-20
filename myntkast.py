from random import randint

def myntkast():
    kast = int(input("Hvor mange myntkast?"))
    kroner=0
    for i in range(kast):
        if randint(0,1) == 1:
            kroner +=1
    print("Antall kast som gav krone:")
    print(kroner)

myntkast()  