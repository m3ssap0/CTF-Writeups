flag = ""
b = ""
for i in range(len(flag)):
    b += bin(ord(flag[i]))[2:].zfill(8)

def drop(b,m):
    return(b[:m]+b[(m+1):])
    
def shift(b, i):
    return(b[i:] + b[:i])

l = len(b)
i = 1
while(i<l):
    m = l%i
    b = drop(b,m)
    b = shift(b,i)
    l = len(b)
    i+=1

print("Compressed data: ",b)


#OUTPUT:
Compressed data: 100001000100110000000100


#SHA-256 of the complete flag is: e67753ef818688790288702b0592a46c390b695a732e1b9fec47a14e2f6f25ae