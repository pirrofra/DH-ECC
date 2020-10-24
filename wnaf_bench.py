import timeit

#Testa DH generando simulando lo scambio di chiavi tra due utenti, e controllando che entrambi generino la stessa chiave z
def key_test(dh):
    try:
        d1,Q1=dh.key_pair_generator()
        d2,Q2=dh.key_pair_generator()
        z1=dh.shared_key_generator(d1,Q2)
        z2=dh.shared_key_generator(d2,Q1)
    except:
        print("*** An error has occurred, and a shared key could not be generated ***")
        raise ValueError("Error during the generation")
    
    if z1==z2:
        #print("-Key["+hex(z1)+"] successfully generated")
        pass
    else:
        print("*** Two different secret key were generated ***")
        raise ValueError("Two different secret key were generated")

#Genera un certo numero di chiavi su di una curva
#con w da 2 a 6
#e misura il tempo di esecuzione con timeit
def bench(curve,times):
    print("Type of curve: "+curve)
    
    for w in range(2,7):
        SETUP='''
from __main__ import key_test
from dh import ECC_CDH
dh=ECC_CDH("'''+curve+'''",wNAF=1,w='''+str(w)+''')'''
        code='''key_test(dh)'''
        wNAF=timeit.timeit(setup=SETUP, stmt=code,number=times)
        print(str(times)+" keys generated using wNAF with w="+str(w)+" in "+str(wNAF)+" seconds")


def multiple_bench(curve,keyTimes,nBench):
    for i in range(0,nBench):
        bench(curve,keyTimes)
    print("----------------------------------------------------")

multiple_bench("curves/p192.xml",1000,5)
multiple_bench("curves/p224.xml",800,5)
multiple_bench("curves/p256.xml",600,5)
multiple_bench("curves/p384.xml",400,5)
multiple_bench("curves/p521.xml",200,5)
