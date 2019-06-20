from math import acos
from math import sin
from math import pi

deg = pi/180

## Trekantløser
def trekant(a,b,c):
    if a > (b+c) or b>(a+c) or c>(a+b):
        print("Ingen løsning")
        return "NA","NA","NA"
    # Vinkel mellom 3 og 1
    A = acos((-pow(a,2) + pow(b,2) + pow(c,2))/(2*b*c))/deg

    print("Vinkel A:")
    print(round(A,1))

    #u =
    B = acos((-pow(b,2) + pow(c,2) + pow(a,2))/(2*a*c))/deg

    print("Vinkel B:")
    print(round(B,1))
    
    #w = 180 - v - u
    C = 180- A - B
    
    print("Vinkel C:")
    print(round(C,1))
    
    #Regner ut areal    
    
    areal=sin(A*deg)*b*c/2    
    
    print("Areal av trekant:")
    print(round(areal,1))
    
    return A,B,C,areal
    
a = int(input("Side a?"))
b = int(input("Side b?"))
c = int(input("Side c?"))

trekant(a,b,c)