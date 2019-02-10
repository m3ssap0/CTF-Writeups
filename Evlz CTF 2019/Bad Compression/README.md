# Evlz CTF 2019 – Bad Compression

* **Category:** Crypto
* **Points:** 150

## Challenge

> This won't be too bad, I guess...
> 
> [File](Bad_Compression.py)

## Solution

For this challenge a [compression script](Bad_Compression.py) is given.

It also contains the output of the script launched on the *content of flag* (i.e. inside of `evlz{}ctf`): `100001000100110000000100`, and the SHA-256 of the complete flag: `e67753ef818688790288702b0592a46c390b695a732e1b9fec47a14e2f6f25ae`.

Basically, you have to reverse the algorithm.

```python
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
```

The first `for` loop takes the code of each char, converts it in binary and pads the string with zeros on the left.

The `shift` method consider the two portions of the string based on one index and shifts their position. Applied two times, it allows to return the original string.

The `drop` method removes a char at a given position. All these positions can be easily calculated at each cycle, using values of `l` and `i` indexes.

The string at the end (`24` bits) is half of the original string (`48` bits). So the searched string is composed by 6 chars (`48 / 8 = 6`) and can't be the complete flag, but only *the content of it* (i.e. inside of `evlz{}ctf`).

An algorithm can be written to put placeholders where the chars were removed. The most significant bit of each byte can be set to 0, because ASCII is represented on 7 bits, so the first could be ignored. Finally, a recursive function can be written to enumerate all possible binary numbers. The searched one is the one with the provided hash in SHA-256.

The complete solver script in Python is the following.

```python
import hashlib

def shift(b, i):
   return(b[i:] + b[:i])
      
def put_placeholder(b, m):
   return(b[:m] + "?" + b[m:])

def find_candidate(b):
   i = len(b)
   while(i > 0):
   
      # Revert the shift operation.
      r = len(b) - i
      b = shift(b, r)
   
      # Put a placeholder where the char was dropped.
      l = len(b) + 1
      m = l % i
      b = put_placeholder(b, m)
   
      i -= 1
   
   return b
   
def set_to_zero_most_significant_bit_of_each_byte(candidate):
   l = list(candidate)
   for p in range(0, len(l)):
      if p % 8 == 0 and l[p] == "?":
         l[p] = "0"
   return "".join(l)

def set_char(string, char, position):
   l = list(string)
   l[position] = char
   return "".join(l)
   
def compose_flag(candidate):
   flag = ""
   i = 0
   while(i < len(candidate)):
      x = int(candidate[i:(i+8)], 2)
      if x < 256:
         flag += chr(x)
         i += 8
      else:
        break
   
   return flag
   
   
def find_flag_r(compressed, candidate, position):

   if position >= len(candidate):
      flag = compose_flag(candidate)
      if len(flag) == 6 and hashlib.sha256("evlz{{{}}}ctf".format(flag)).hexdigest() == "e67753ef818688790288702b0592a46c390b695a732e1b9fec47a14e2f6f25ae":
         print ">>> Found! >>> {}".format(candidate)
         print ">>>>>>>>>>>>>> evlz{{{}}}ctf".format(flag)
   else:
      if candidate[position] == "?":
          candidate = set_char(candidate, "0", position) 
          find_flag_r(compressed, candidate, position + 1)
          candidate = set_char(candidate, "1", position) 
          find_flag_r(compressed, candidate, position + 1)
          candidate = set_char(candidate, "?", position) 
      else:
         find_flag_r(compressed, candidate, position + 1)
       
       
     
compressed = "100001000100110000000100"
candidate = find_candidate(compressed)
print "Dirty candidate = {}".format(candidate)
candidate = set_to_zero_most_significant_bit_of_each_byte(candidate)
print "Clean candidate = {}".format(candidate)
find_flag_r(compressed, candidate, 0)
```

It will print the flag.

```
Dirty candidate = ????00?0?0?1000????????1001?1?00??00?0?00?1001??
Clean candidate = 0???00?000?1000?0??????1001?1?000?00?0?00?1001??
>>> Found! >>> 001100100011000001101111001110000100000001100100
>>>>>>>>>>>>>> evlz{20o8@d}ctf
```