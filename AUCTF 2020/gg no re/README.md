# AUCTF 2020 – gg no re

* **Category:** web
* **Points:** 50

## Challenge

> http://challenges.auctf.com:30022
> 
> A junior dev built this site but we want you to test it before we send it to production.
> 
> Author: shinigami

## Solution

Analyzing the HTML of the page, you can discover a [JavaScript script](authentication.js).

```html
<html>
  <head>
    <script>authentication.js</script>
  </head>
  <body>
    <center><h1>Nothing to see here</h1></center>
  </body>
</html>
```

The code at `http://challenges.auctf.com:30022/authentication.js` is obfuscated.

```javascript
var _0x44ff=['TWFrZSBhIEdFVCByZXF1ZXN0IHRvIC9oaWRkZW4vbmV4dHN0ZXAucGhw','aW5jbHVkZXM=','bGVuZ3Ro','bG9n'];(function(_0x43cf52,_0x44ff2a){var _0x2ad1c9=function(_0x175747){while(--_0x175747){_0x43cf52['push'](_0x43cf52['shift']());}};_0x2ad1c9(++_0x44ff2a);}(_0x44ff,0x181));var _0x2ad1=function(_0x43cf52,_0x44ff2a){_0x43cf52=_0x43cf52-0x0;var _0x2ad1c9=_0x44ff[_0x43cf52];if(_0x2ad1['UmZuYF']===undefined){(function(){var _0x4760ee=function(){var _0x335dc0;try{_0x335dc0=Function('return\x20(function()\x20'+'{}.constructor(\x22return\x20this\x22)(\x20)'+');')();}catch(_0x3b3b3e){_0x335dc0=window;}return _0x335dc0;};var _0x1ecd5c=_0x4760ee();var _0x51e136='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x1ecd5c['atob']||(_0x1ecd5c['atob']=function(_0x218781){var _0x1c7e70=String(_0x218781)['replace'](/=+$/,'');var _0x1fccf7='';for(var _0x2ca4ce=0x0,_0x55266e,_0x546327,_0x17b8a3=0x0;_0x546327=_0x1c7e70['charAt'](_0x17b8a3++);~_0x546327&&(_0x55266e=_0x2ca4ce%0x4?_0x55266e*0x40+_0x546327:_0x546327,_0x2ca4ce++%0x4)?_0x1fccf7+=String['fromCharCode'](0xff&_0x55266e>>(-0x2*_0x2ca4ce&0x6)):0x0){_0x546327=_0x51e136['indexOf'](_0x546327);}return _0x1fccf7;});}());_0x2ad1['hdhzHi']=function(_0x5d9b5f){var _0x24b0b1=atob(_0x5d9b5f);var _0x5c5f21=[];for(var _0x390988=0x0,_0xd8eac0=_0x24b0b1['length'];_0x390988<_0xd8eac0;_0x390988++){_0x5c5f21+='%'+('00'+_0x24b0b1['charCodeAt'](_0x390988)['toString'](0x10))['slice'](-0x2);}return decodeURIComponent(_0x5c5f21);};_0x2ad1['wrYKfR']={};_0x2ad1['UmZuYF']=!![];}var _0x175747=_0x2ad1['wrYKfR'][_0x43cf52];if(_0x175747===undefined){_0x2ad1c9=_0x2ad1['hdhzHi'](_0x2ad1c9);_0x2ad1['wrYKfR'][_0x43cf52]=_0x2ad1c9;}else{_0x2ad1c9=_0x175747;}return _0x2ad1c9;};function authenticate(_0x335dc0){if(validate(_0x335dc0)){console[_0x2ad1('0x2')](_0x2ad1('0x3'));}};function validate(_0x3b3b3e){return _0x3b3b3e[_0x2ad1('0x1')]>=0x5&&_0x3b3b3e[_0x2ad1('0x0')]('$');}
```

The initial array contains base64 encoded strings.

```javascript
var _0x44ff=['TWFrZSBhIEdFVCByZXF1ZXN0IHRvIC9oaWRkZW4vbmV4dHN0ZXAucGhw','aW5jbHVkZXM=','bGVuZ3Ro','bG9n'];
```

Decoding them, you will obtain the following.

```javascript
var _0x44ff=['Make a GET request to /hidden/nextstep.php','includes','length','log'];
```

So you can discover another endpoint: `http://challenges.auctf.com:30022/hidden/nextstep.php` to contact.

```
GET /hidden/nextstep.php HTTP/1.1
Host: challenges.auctf.com:30022
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 22:51:00 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
ROT13: Znxr n CBFG erdhrfg gb /ncv/svany.cuc
Content-Length: 15
Connection: close
Content-Type: text/html; charset=UTF-8

Howdy neighbor!
```

The HTTP response contains a ROT13 encrypted message in HTTP headers that can be easily decrypted.

```
Make a POST request to /api/final.php
```

Performing the `POST` request you will get the following answer.

```
POST /api/final.php HTTP/1.1
Host: challenges.auctf.com:30022
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0
Content-Type: application/x-www-form-urlencoded

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 23:24:33 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Content-Length: 43
Connection: close
Content-Type: text/html; charset=UTF-8

Send a request with the flag variable set 
```

Changing the `POST` request with a `flag` variable set will give you the flag.

```
POST /api/final.php HTTP/1.1
Host: challenges.auctf.com:30022
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 11
Content-Type: application/x-www-form-urlencoded

flag=aaaaaa

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 23:23:19 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Content-Length: 30
Connection: close
Content-Type: text/html; charset=UTF-8

auctf{1_w@s_laZ_w1t_dis_0N3} 
```