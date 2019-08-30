class Point:
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x
        self.y=y

class EllipticCurve:
    __a=0
    __b=0
    __p=0
    
    def __init__(self,a,b,n):
        self.__a=a
        self.__b=b
        self.__p=n
    
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

    def double (self,p):
        if p.x==0 and p.y==0:
            return Point(0,0)
        lmb_n= ((3*(p.x**2))+self.__a) % self.__p
        lmb_d=(2*p.y) % self.__p
        if lmb_d==0:
            return Point(0,0)
        lmb_d_inv=self.__mulinv(lmb_d)
        lmb=(lmb_n*lmb_d_inv) %self.__p
        xr=((lmb**2) - (2*p.x)) % self.__p
        yr=((lmb*(p.x-xr)) -p.y) % self.__p
        return Point(xr,yr)
    
    def sum(self, p,q):
        if(p.x==0 and p.y==0):
            return q
        if(q.x==0 and q.y==0):
            return p
        if(p.x==q.x and p.y==q.y):
            return self.double(p)
        lmb_n =  (q.y - p.y) % self.__p
        lmb_d = (q.x - p.x) % self.__p
        if(lmb_d==0):
            return Point(0,0)
        lmd_d_inv=self.__mulinv(lmb_d)
        lmb=(lmb_n*lmd_d_inv) % self.__p
        xr=((lmb**2) - (p.x) - (q.x) ) % self.__p
        yr=(lmb*(p.x-xr) - p.y) % self.__p
        return Point(xr,yr)

    def double_and_add(self,d,P):
        R=Point(0,0)
        while d!=0:
            if d % 2 == 1:
                R=self.sum(R,P)
            P=self.double(P)
            d=d//2
        return R

    def isOnCurve(self,P):
        arg1=P.y**2 % self.__p
        arg2=((P.x**3) + (self.__a*P.x)+self.__b) % self.__p
        if arg1==arg2:
            return True
        else:
            return False


