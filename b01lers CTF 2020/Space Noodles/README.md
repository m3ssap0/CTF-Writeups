# b01lers CTF 2020 – Space Noodles

* **Category:** web
* **Points:** 200

## Challenge

> What do you get when you cross spaghetti with zero g's?
> 
> http://web.ctf.b01lers.com:1003/

## Solution

This was a guessing challenge and I didn't like it very much.

Trying to connect to the homepage will give you an error of HTTP method not allowed.

```
GET / HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 121
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 10:24:44 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Not Allowed</title>
<h1>Not Allowed</h1>
<p>Cant GET /</p>
```

If you try a wrong HTTP verb, the server will return all the allowed methods.

```
POTATOE / HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.0 405 METHOD NOT ALLOWED
Content-Type: text/html; charset=utf-8
Allow: GET, HEAD, PUT, PATCH, CONNECT, OPTIONS, TRACE, DELETE, POST
Content-Length: 178
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 10:26:17 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
```

Trying each method, you can discover that some of them, i.e. `POST` and `PUT`, will return a different result.

```
POST / HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 570
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 10:31:13 GMT

  <html>
  </body>
      <body>
        <text><p></text>text ? pleas test teh follwing five roots<p>,</p>
  <list>
    <one>

circle</one>
    <enter>
    <enter>
    <sendkey(enter)>

two
  I'm am making an a pea eye and its grate

         PHP is the best
      <php?> printf(hello world) </php>
square<?/p>two


  :pleasequithelpwww.google.
com/seaerch

    how to exit
vim/quit
  :wqwhy isnt it working:wq:wq:wq:qw?

      </body>
                                                                                                                                </html>
```

At this point you have to guess that the following endpoints are present:
* `/circle/one/`;
* `/two/`;
* `/square/`;
* `/com/seaerch/`;
* `/vim/quit/`.

For each endpoint, you have to try all HTTP verbs in order to discover the correct one to use.

The `/circle/one/` endpoint will return a [PDF file](http_web.ctf.b01lers.com_1003_circle_one.pdf).

```
OPTIONS /circle/one/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.0 200 OK
Content-Length: 3322704
Content-Type: application/pdf
Last-Modified: Tue, 10 Mar 2020 20:13:28 GMT
Cache-Control: public, max-age=43200
Expires: Sun, 15 Mar 2020 02:03:47 GMT
ETag: "1583871208.0-3322704-1012733123"
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 14:03:47 GMT

%PDF-1.3
```

The PDF says: `Put Your Best Food Forward With HEINZ KETCHUP`. At this point I had no idea of what to do next.

Two different answers can be obtained on `/two/` endpoint with `PUT` and `CONNECT` HTTP verbs.

```
PUT /two/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 15
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 10:55:40 GMT

Put the dots???
```

The `CONNECT /two/` request will return a PNG image.

```
CONNECT /two/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.0 200 OK
Content-Length: 67798
Content-Type: image/png
Last-Modified: Tue, 10 Mar 2020 20:13:28 GMT
Cache-Control: public, max-age=43200
Expires: Sat, 14 Mar 2020 22:56:58 GMT
ETag: "1583871208.0-67798-3337817112"
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 10:56:58 GMT

   PNG
```

![two.png](two.png)

The image contains the string `up_on_noodles_`, that is a part of the flag.

The `/square/` endpoint will return a PNG image with a crossword puzzle.

```
DELETE /square/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.0 200 OK
Content-Length: 211123
Content-Type: image/png
Last-Modified: Tue, 10 Mar 2020 20:13:28 GMT
Cache-Control: public, max-age=43200
Expires: Sat, 14 Mar 2020 23:12:50 GMT
ETag: "1583871208.0-211123-3343453223"
Server: Werkzeug/1.0.0 Python/3.7.6
Date: Sat, 14 Mar 2020 11:12:50 GMT

   PNG
```

![square.png](square.png)

The solution is the following.

```
    E
    S
    I
    R
    P
  E R
  C E
  A T
E P N
TASTES
 L A U
 D U L
 E   A
 R   C
 A   O
 A
 N
```

The `/com/seaerch/` endpoint will return the following webpage.

```
GET /com/seaerch/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 94
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 15:02:41 GMT

<htlm>

,,,,,,,,,<search> <-- comment for search --!>:

  ERROR </> search=null</end>

</html>
```

At this point, you have to guess that an `application/x-www-form-urlencoded` parameter must be used to perform the search operation

```
GET /com/seaerch/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 10
Content-Type: application/x-www-form-urlencoded

search=foo

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 142
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 20:02:46 GMT

<htlm>

,,,,,,,,,<search> <-- comment for search --!>:

  <query> foo is not a good search, please use this one instead: 'flag' <try>

</html>
```

Using the `flag` value will give you another part of the flag.

```
GET /com/seaerch/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
Comment: foo
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 11
Content-Type: application/x-www-form-urlencoded

search=flag

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 126
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 20:03:13 GMT

<htlm>

,,,,,,,,,<search> <-- comment for search --!>:

  <query> good search</query>
  results: <p>_good_in_s</p>:w


</html>
```

The `/vim/quit/` endpoint will tell you to use a query parameter.

```
TRACE /vim/quit/ HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: session=0
Upgrade-Insecure-Requests: 1

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 109
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 19:27:54 GMT

   <hteeemel<body>>

                    <wrong>uh oh 
                  ?exit=null
            </wrong>

</>
```

Passing a random value will let you to discover that a *vim* command must be used.

```
TRACE /vim/quit/?exit=foo HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 104
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 19:28:49 GMT

   <hteeemel<body>>

       <erroror><p>E492: Not an editor command: foo</p>
 </errorror>
 </flag>


</>
```

Considering that the name of the parameter is `exit`, you have to discover that `:wq` is the correct value to use.

```
TRACE /vim/quit/?exit=:wq HTTP/1.1
Host: web.ctf.b01lers.com:1003
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 102
Server: Werkzeug/1.0.0 Python/3.7.7
Date: Sat, 14 Mar 2020 19:30:59 GMT

   <hteeemel<body>>

      <flag> well done wait </flag>
<text> this one/> <flag>pace_too}</flag>

</>
```

Putting everything together will give you the following.

```
1 2              3      4          5   
  up_on_noodles_ tastes _good_in_s pace_too}
```

At this point you can easily guess the first part of the flag (referred to the PDF).

```
pctf{ketchup_on_noodles_tastes_good_in_space_too}
```