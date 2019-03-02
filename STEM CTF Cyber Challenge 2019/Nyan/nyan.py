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