# b01lers CTF 2020 – Scrambled

* **Category:** web
* **Points:** 200

## Challenge

> I was scanning through the skies. And missed the static in your eyes. Something blocking your reception. It's distorting our connection. With the distance amplified. Was it all just synthesized? And now the silence screams that you are gone. You've tuned me out. I've lost your frequency.
> 
> http://web.ctf.b01lers.com:1002/

## Solution

Analyzing the webpage, two strange cookies can be discovered: 
* `frequency`;
* `transmissions`.

`frequency` is incremented at each refresh, `transmissions` contains a fixed part – at the beginning and at the end – and a variable part in the middle.

```
kxkxkxkxshle22kxkxkxkxsh
^^^^^^^^^^    ^^^^^^^^^^
  fixed   ^^^^  fixed
        variable
```

If you enumerate a great amount of cookies, you can notice that the format of variable part is the following:
* previous char of the flag;
* actual char of the flag;
* index of the actual char.

So you can write a [script](scrambled.py) to retrieve all chars and compose the flag.

```python
#!/usr/bin/python

import re
import requests
import urllib.parse

target_endpoint = "http://web.ctf.b01lers.com:1002/"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
}
user_agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);"
noise = "kxkxkxkxsh"

cookies = ""
transmissions = []
i = 0

# Reading transmissions.
while len(transmissions) < 68:
    
    print("[*] Step {}.".format(i))
    i += 1
    if len(cookies) > 0:
        r = requests.get(target_endpoint, headers=headers, cookies=cookies)
    else:
        r = requests.get(target_endpoint, headers=headers)
    cookies = r.cookies
    
    transmission = None
    for cookie in cookies:
        print("[*] Found cookie: {}={}".format(cookie.name, cookie.value))
        if cookie.name == "transmissions" and cookie.value != "0":
            transmission = urllib.parse.unquote(cookie.value.replace(noise, ""))
    if transmission is not None:
        print("[*] Transmission value: {}".format(transmission))
        transmissions.append(transmission)
        transmissions = list(dict.fromkeys(transmissions)) # Removing duplicates.
        print("[*] Different transmissions read: ".format(len(transmissions)))

print(len(transmissions))
print(transmissions)

# Composing flag.
flag = "p"
char_index = 0
while flag == "" or flag[-1] != "}":
    for transmission in transmissions:
        index = transmission[2:]
        if index == str(char_index):
            flag += transmission[1]
            char_index += 1
            print("[*] Composing flag: {}".format(flag))
            break

print("[*] The FLAG is: {}".format(flag))
```

The flag is the following.

```
pctf{Down_With_the_Fallen,Carnivore,Telescope,It_Has_Begun,My_Demons}
```