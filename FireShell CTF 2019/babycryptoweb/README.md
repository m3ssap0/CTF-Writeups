# FireShell CTF 2019 – babycryptoweb

* **Category:** misc
* **Points:** 60

## Challenge

> Can you help me recover the flag?
>
> [https://babycryptoweb.challs.fireshellsecurity.team/](https://babycryptoweb.challs.fireshellsecurity.team/)

## Solution

The challenge shows a web page with the following source code.

```php
<?php

$code = '$kkk=5;$s="e1iwZaNolJeuqWiUp6pmo2iZlKKulJqjmKeupalmnmWjVrI=";$s=base64_decode($s);$res="";for($i=0,$j=strlen($s);$i<$j;$i++){$ch=substr($s,$i,1);$kch=substr($kkk,($i%strlen($kkk))-1,1);$ch=chr(ord($ch)+ord($kch));$res.=$ch;};echo $res;';
    
if (isset($_GET['p']) && isset($_GET['b']) && strlen($_GET['b']) === 1 && is_numeric($_GET['p']) && (int) $_GET['p'] < strlen($code)) {
    $p = (int) $_GET['p'];
    $code[$p] = $_GET['b'];
    eval($code);
} else {
    show_source(__FILE__);
}

?> 
```

The evaluated string into `$code` variable is the following.

```php
$kkk = 5;
$s="e1iwZaNolJeuqWiUp6pmo2iZlKKulJqjmKeupalmnmWjVrI=";
$s=base64_decode($s);
$res="";
for($i=0,$j=strlen($s);$i<$j;$i++) {
  $ch=substr($s,$i,1);
  $kch=substr($kkk,($i%strlen($kkk))-1,1);
  $ch=chr(ord($ch)+ord($kch));
  $res.=$ch;
};
echo $res;
```

Trying to understand the source code, following considerations can be made.

`p` and `b` are two parameters of the script.

`p` must be numeric and lesser than the evalued code dimension, i.e. it is a position into that code.

`b` is a char that must be replaced into that code.

The first char of the flag must be a `F`, so the result of `ord($ch)+ord($kch)` operation must be `70` (i.e. the decimal code of the ASCII letter `F`).

The first char of the base64 decoded string is represented by `123` decimal code, i.e. it's a `{`. 

Some considerations can be done about `$kch=substr($kkk,($i%strlen($kkk))-1,1);` instruction:
* `$i%strlen($kkk)` will always be equals to `0` because `$kkk` has one char only;
* the substring operation will become `substr($kkk,-1,1)` and it will always return the char `5` (i.e. one char from the end of `$kkk` string);
* hence `ord($kch)` will be always `53`.

So, if `ord($ch)` for the first char is `123`, `ord($kch)` is always `53` and the result of the operation for the first char must be `70`, the wrong part of the evaluated script is the `+` char of the `$ch=chr(ord($ch)+ord($kch));` operation, because `123 - 53 = 70`.

The position of that char is `201`; you could try to replace it with `-` char.

The following URL can be used to exploit the script.

`https://babycryptoweb.challs.fireshellsecurity.team/?p=201&b=-`

And it will reveal the flag.

```
F#{0n3_byt3_ru1n3d_my_encrypt1i0n!}
```