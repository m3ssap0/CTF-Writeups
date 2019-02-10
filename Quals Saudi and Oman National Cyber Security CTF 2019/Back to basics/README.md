# Quals Saudi and Oman National Cyber Security CTF 2019 – Back to basics

* **Category:** Web Security
* **Points:** 50

## Challenge

> not pretty much many options. No need to open a link from a browser, there is always a different way
>
> [http://35.197.254.240/backtobasics](http://35.197.254.240/backtobasics)

## Solution

Opening the URL with browser will redirect to Google.

*curl* should be used to GET the page.

```
$ curl -X GET -i http://35.197.254.240/backtobasics/
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Thu, 07 Feb 2019 20:44:45 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Allow: GET, POST, HEAD,OPTIONS


<script> document.location = "http://www.google.com"; </script>
```

The URL seems to allow following HTTP operations: `GET`, `POST`, `HEAD`, `OPTIONS`.

Using `POST` will return the following.

```
$ curl -X POST -i http://35.197.254.240/backtobasics/
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Thu, 07 Feb 2019 20:42:56 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Allow: GET, POST, HEAD,OPTIONS

<!--
var _0x7f88=["","join","reverse","split","log","ceab068d9522dc567177de8009f323b2"];function reverse(_0xa6e5x2){flag= _0xa6e5x2[_0x7f88[3]](_0x7f88[0])[_0x7f88[2]]()[_0x7f88[1]](_0x7f88[0])}console[_0x7f88[4]]= reverse;console[_0x7f88[4]](_0x7f88[5])
-->
```

The returned JavaScript can be written like the following to retrieve the flag.

```javascript
var _0x7f88=["","join","reverse","split","log","ceab068d9522dc567177de8009f323b2"];

function reverse(_0xa6e5x2) {
  flag= _0xa6e5x2[_0x7f88[3]](_0x7f88[0])[_0x7f88[2]]()[_0x7f88[1]](_0x7f88[0])
  console.log(flag)
}

//console[_0x7f88[4]]= reverse;
//console[_0x7f88[4]](_0x7f88[5]);
reverse(_0x7f88[5]);
```

The flag is the following.

```
2b323f9008ed771765cd2259d860baec
```