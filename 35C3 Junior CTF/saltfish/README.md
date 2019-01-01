# 35C3 Junior CTF – saltfish

* **Category:** Web
* **Points:** 62 (variable)

## Challenge

> "I have been told that the best crackers in the world can do this under 60 minutes but unfortunately I need someone who can do this under 60 seconds." - Gabriel
>
> http://35.207.89.211

## Solution

The page shows the PHP snippet of which is composed (I added the comments with numbers on interesting lines of code).

```PHP
<?php
  require_once('flag.php');
  if ($_ = @$_GET['pass']) {                    /* #1 */
    $ua = $_SERVER['HTTP_USER_AGENT'];
    if (md5($_) + $_[0] == md5($ua)) {          /* #2 */
      if ($_[0] == md5($_[0] . $flag)[0]) {     /* #3 */
        echo $flag;
      }
    }
  } else {
    highlight_file(__FILE__);
  }
```

The `if` statement *#1* is useless for the analysis. `$_` is a normal variable populated with `pass` URL parameter content and the `@` clause does not affect anything in our scenario.

The `if` statement *#2* can be bypassed using the same value for `pass` URL parameter and for the User-Agent, because PHP's `==` gets confused with type conversions, lol.

The `if` statement *#3* contains the secret flag into a MD5 calculation, so it could seem hard to bypass, but:
* the MD5 hash can only have hex values from `0` to `f`;
* only the first char of two strings is considered in the comparison.

So the value of `$_[0]` can be between `0` and `f` only.

Trying single chars, from `0` to `f`, for the input of `pass` and User-Agent header, will reveal that `b` is the char that returns the flag.

```
35c3_password_saltf1sh_30_seconds_max
```