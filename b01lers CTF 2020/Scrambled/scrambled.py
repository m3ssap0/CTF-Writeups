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