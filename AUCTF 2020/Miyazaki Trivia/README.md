# AUCTF 2020 – Miyazaki Trivia

* **Category:** web
* **Points:** 50

## Challenge

> http://challenges.auctf.com:30020
> 
> Here's a bit of trivia for you vidya game nerds.
> 
> Author: shinigami

## Solution

The website prints a message.

```html
<doctype html>
<html>
	<title>AUCTF</title>
	<body>
		<h1>Find this special file.</h1>
	</body>
</html>
```

Connecting to `http://challenges.auctf.com:30020/robots.txt` will give the following message.

```
VIDEO GAME TRIVIA: What is the adage of Byrgenwerth scholars?

MAKE a GET request to this page with a header named 'answer' to submit your answer.
```

The answer to the trivia is: `Fear the Old Blood`. So you can perform the requested HTTP GET and you will get the flag.

```
GET /robots.txt HTTP/1.1
Host: challenges.auctf.com:30020
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
answer: Fear the Old Blood

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:19:14 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Content-Length: 48
Connection: close
Content-Type: text/html; charset=UTF-8

Master Willem was right.auctf{f3ar_z_olD3_8l0oD}
```