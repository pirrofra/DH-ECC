from dh import *

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
        print("-Key["+hex(z1)+"] successfully generated")
    else:
        print("*** Two different secret key were generated ***")
        raise ValueError("Two different secret key were generated")

dh=ECC_CDH("curves/p256.xml")

for i in range(0,1000):
    key_test(dh)

print("All keys were succesfully generated")