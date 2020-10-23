#Classe che definisce un Punto, e conserva le coordinate x e y
class Point:
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x
        self.y=y

#Classe che definisce una curva ellittica e le operazioni elementari possibili in essa.
class EllipticCurve:
    __a=0
    __b=0
    __p=0
    
    def __init__(self,a,b,n):
        self.__a=a
        self.__b=b
        self.__p=n
    
    #Inverso in modulo p tramite l'algoritmo di Euclide Esteso
    def __mulinv(self,x):
        t=0
        r=self.__p
        new_t=1
        new_r=x

        while new_r != 0:
            q= r // new_r
            t,new_t=new_t, t-(q*new_t)
            r,new_r=new_r, r-(q*new_r)
        
        if t<0:
            return t+self.__p
        else:
            return t

    #calcolo del doppio di un punto P
    def double (self,p):
        #il doppio del punto all'infinito, è il punto all'infinito
        if p.x==0 and p.y==0:
            return Point(0,0)
        lmb_n= ((3*(p.x**2))+self.__a) #numeratore del lamba, della formula del raddoppio
        lmb_d=(2*p.y) % self.__p #denominatore del lamba, della formula del raddoppio
        if lmb_d==0: #se il denominatore è 0, la coordinata y di P era 0, quindi la tangente incontra la curva al punto all'infinito
            return Point(0,0)
        #per effettuare il calcolo di lamba, in modulo, dobbiamo calcolare l'inverso e poi moltiplicare
        #non possiamo dividere
        lmb_d_inv=self.__mulinv(lmb_d) 
        lmb=(lmb_n*lmb_d_inv) 
        xr=((lmb**2) - (2*p.x)) % self.__p
        yr=((lmb*(p.x-xr)) -p.y) % self.__p
        return Point(xr,yr)
    
    def sum(self, p,q):
        #controllo se P e Q sono punti all'infinito
        if(p.x==0 and p.y==0):
            return q
        if(q.x==0 and q.y==0):
            return p
        #Controllo se la somma che sto facendo in realtà è un raddoppio
        if(p.x==q.x and p.y==q.y):
            return self.double(p)
        lmb_n =  (q.y - p.y) #numeratore del lamba, della formula della somma
        lmb_d = (q.x - p.x) % self.__p #denominatore del lamba, della formula della somma
        if(lmb_d==0): #se il denominatore è 0, P e Q sono opposti quindi la loro somma è il punto all'infinito
            return Point(0,0)
        #per effettuare il calcolo di lamba, in modulo, dobbiamo calcolare l'inverso e poi moltiplicare
        #non possiamo dividere
        lmd_d_inv=self.__mulinv(lmb_d)
        lmb=(lmb_n*lmd_d_inv)
        xr=((lmb**2) - (p.x) - (q.x) ) % self.__p
        yr=(lmb*(p.x-xr) - p.y) % self.__p
        return Point(xr,yr)

    #Algortimo double and add per moltiplicare
    def __double_and_add(self,d,P):
        R=Point(0,0)
        while d!=0:
            if d % 2 == 1:
                R=self.sum(R,P)
            P=self.double(P)
            d=d//2
        return R

    #Verifica la presenza di un punto sulla curva sostituendo x e y nell'equazione della curva.
    def isOnCurve(self,P):
        arg1=P.y**2 % self.__p
        arg2=((P.x**3) + (self.__a*P.x)+self.__b) % self.__p
        if arg1==arg2:
            return True
        else:
            return False

    def mul(self,d,P):
        return self.__double_and_add(d,P)

