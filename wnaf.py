from curve import *

#Classe che estende EllipticCurve, ed implementa wNAF
class WNAF(EllipticCurve):

    #questo costruttore richiede in più la w, rispetto alla sua superclasse
    def __init__(self,a,b,n,w):
        super(WNAF,self).__init__(a,b,n)
        self.__w=w
        self.__expw=pow(2,w)

    #Funzione che implementa il modulo in segno
    def __mod(self,d):
        mod=d % self.__expw
        if  mod >= self.__expw//2:
            return mod -self.__expw
        else:
            return mod
    
    #Funziona che calcola il w-NAF di d
    def __NAF(self,d):
        i=0
        naf=[] #array che conserva le cifre k della rappresentazione, di dimensione i
        while d>0:
            if(d % 2)==1:
                d_i=self.__mod(d)
                naf.append(d_i)
                d=d-d_i
            else:
                naf.append(0)
            d=d//2
            i=i+1
        return (i-1,naf)

    #Pre calcoli dei punti {P,3P,5P.... } e {-P,-3P,-5P....}
    def __precalc(self,P):
        precalculated={} #dizionario che conserva i punti
        i=1
        double_p=self.double(P)
        Q=P
        while(i<=self.__expw-1):
            precalculated[i]=Q
            precalculated[-i]=Point(Q.x,0-Q.y) #-P ha la stessa coordinata x di P, ma y di segno opposto.
            Q=self.sum(Q,double_p)
            i=i+2
        return precalculated

    #algoritmo per la moltiplicazione
    def __wNAF(self,d,P):
        (i,naf)=self.__NAF(d) #calcola il w-NAF
        precalculated=self.__precalc(P) #precalcolo dei punti

        #Ottiene Q a partire dalla sua rappresentazione w-NAF
        Q=Point(0,0)
        while(i>=0):
            Q=self.double(Q)
            di=naf[i]
            if(di != 0):
                Q=self.sum(Q,precalculated[di])
            i=i-1
        return Q

    #sovrascrive mul affinchè utilizzi wNAF e non double-and-add
    def mul(self,d,P):
        return self.__wNAF(d,P)