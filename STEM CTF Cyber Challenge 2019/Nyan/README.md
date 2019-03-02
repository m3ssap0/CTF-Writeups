# STEM CTF Cyber Challenge 2019 – Nyan

* **Category:** Grab Bag
* **Points:** 50

## Challenge

> Nyayanayanayanayanayanayanayan
> 
> ssh ctf@138.247.13.114

## Solution

Connecting in SSH will trigger a wonderful 8 bit *Nyan Cat* representation.

The flag is probably hidden in the data flow. To intercept it, the data exchanged with the server must be analyzed.

A [Python script](nyan.py) can be written to help on this.

```python
import re
from pwn import *

l = listen()
shell =  ssh(host="138.247.13.114", user="ctf", password="ctf")
sh = shell.run('sh')
while True:
   received = sh.recvline()
   if "MCA{" in received:
      x = re.findall("MCA\{.+\}", received)
      print x[0]
      break
```

The flag is the following.

```
MCA{Airadaepohh8Sha}
```