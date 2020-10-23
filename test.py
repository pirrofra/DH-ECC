from dh import ECC_CDH
import time

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


curve="curves/p256.xml"
dh=ECC_CDH(curve)

start_time = time.time()
for i in range(0,200):
    key_test(dh)
d_a_a=time.time() - start_time
print("*** All keys correctley generated ***")
print("200 keys generated using Double-and-Add in "+str(d_a_a)+" milliseconds")



dh=ECC_CDH(curve,wNAF=1)
start_time = time.time()
for i in range(0,200):
    key_test(dh)
wNAF=time.time() - start_time
print("*** All keys correctley generated ***")
print("200 keys generated using wNAF in "+str(wNAF)+" milliseconds")

if(wNAF<d_a_a):
    print("*** WNAF IS FASTER***")
else:
    print("*** DOUBLE AND ADD IS FASTER***")