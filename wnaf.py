from curve import *

class WNAF(EllipticCurve):

    def __init__(self,a,b,n,w):
        super(WNAF,self).__init__(a,b,n)
        self.__w=w
        self.__expw=pow(2,w)

    def __mod(self,d):
        mod=d % self.__expw
        if  mod >= self.__expw//2:
            return mod -self.__expw
        else:
            return mod
    
    def __NAF(self,d):
        i=0
        naf=[]
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

    def __precalc(self,P):
        precalculated={}
        i=1
        double_p=self.double(P)
        Q=P
        while(i<=self.__expw-1):
            precalculated[i]=Q
            precalculated[-i]=Point(Q.x,0-Q.y)
            Q=self.sum(Q,double_p)
            i=i+2
        return precalculated

    def __wNAF(self,d,P):
        (i,naf)=self.__NAF(d)
        precalculated=self.__precalc(P)

        Q=Point(0,0)
        while(i>=0):
            Q=self.double(Q)
            di=naf[i]
            if(di != 0):
                Q=self.sum(Q,precalculated[di])
            i=i-1
        return Q

    
    def mul(self,d,P):
        return self.__wNAF(d,P)