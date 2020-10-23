from curve import *
from wnaf import *
import os
import struct
import sys
import xml.etree.ElementTree as ET

class ECC_CDH:
    __ecc=None
    __n=0
    __G=None
    #Costruttore
    def __init__(self,path,wNAF=0):
        tree=ET.parse(path)
        curve=tree.getroot()
        #Lettera dei valori dal file .xml in path
        p=int(curve.find("p").text,10)
        a=int(curve.find("a").text,10)
        b=int(curve.find("b").text,10)
        n=int(curve.find("n").text,10)
        G=curve.find("G")
        x=int(G.find("x").text,10)
        y=int(G.find("y").text,10)
        #scelta se utilizzare wNAF o meno, in base al valore del parametro
        if wNAF==0:
            self.__ecc=EllipticCurve(a,b,p)
        else:
            w=int(curve.find("w").text,10)
            self.__ecc=WNAF(a,b,p,w)
        self.__n=n
        self.__G=Point(x,y)

    #Funzione che genera la chiave pubblica Q, e il segreto d come specificato dal NIST
    def key_pair_generator(self):
        L=self.__n.bit_length()+64
        returned_bits=os.urandom(L) #funzione crittograficamente sicura
        c=int.from_bytes(returned_bits,byteorder=sys.byteorder, signed=False)
        d= (c % (self.__n -1))+1 #calcolo di d, a partire dal valore randomico ottenuto
        Q= self.__ecc.mul(d,self.__G) #Q=d*G
        #Errori lanciati se la chiave generata è 0, o è generato un punto non appartente alla curva
        #Controllo richiesto dal NIST
        if Q.x==0 and Q.y==0:
            raise ValueError("Public Key is zero")
        elif(not self.__ecc.isOnCurve(Q)):
            raise ValueError("Invalid Point")
        return d,Q

    #Funzione che ottiene la chiave segreta condiva a partire dal proprio segreto d e dalla chiave pubblica Q di un altro utente
    def shared_key_generator(self,d,Q):
        P=self.__ecc.mul(d,Q) #P=d*Q
        if P.x==0 and P.y==0:
            raise ValueError("P is zero")
        z=P.x #si restituisce solo la coordinata x, come richiesto dal NIST
        return z


