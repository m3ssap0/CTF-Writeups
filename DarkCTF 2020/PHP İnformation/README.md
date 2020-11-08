# DarkCTF 2020 – PHP İnformation

* **Category:** web
* **Points:** 198

## Challenge

> Let's test your php knowledge.
> 
> Flag Format: DarkCTF{}
> 
> http://php.darkarmy.xyz:7001

## Solution

Connecting to the web page will give you the following PHP source code.

```php
<?php

include "flag.php";

echo show_source("index.php");


if (!empty($_SERVER['QUERY_STRING'])) {
    $query = $_SERVER['QUERY_STRING'];
    $res = parse_str($query);
    if (!empty($res['darkctf'])){
        $darkctf = $res['darkctf'];
    }
}

if ($darkctf === "2020"){
    echo "<h1 style='color: chartreuse;'>Flag : $flag</h1></br>";
}

if ($_SERVER["HTTP_USER_AGENT"] === base64_decode("MjAyMF90aGVfYmVzdF95ZWFyX2Nvcm9uYQ==")){
    echo "<h1 style='color: chartreuse;'>Flag : $flag_1</h1></br>";
}


if (!empty($_SERVER['QUERY_STRING'])) {
    $query = $_SERVER['QUERY_STRING'];
    $res = parse_str($query);
    if (!empty($res['ctf2020'])){
        $ctf2020 = $res['ctf2020'];
    }
    if ($ctf2020 === base64_encode("ZGFya2N0Zi0yMDIwLXdlYg==")){
        echo "<h1 style='color: chartreuse;'>Flag : $flag_2</h1></br>";
                
        }
    }



    if (isset($_GET['karma']) and isset($_GET['2020'])) {
        if ($_GET['karma'] != $_GET['2020'])
        if (md5($_GET['karma']) == md5($_GET['2020']))
            echo "<h1 style='color: chartreuse;'>Flag : $flag_3</h1></br>";
        else
            echo "<h1 style='color: chartreuse;'>Wrong</h1></br>";
    }



?>
```

You have to satisfy all checks to print the flag.

For the last check you have to find [two colliding MD5 strings](https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value). Based on [this example](https://ideone.com/UyP22Z) you can write your [script](md5_collisions.php) to generate the URL-encoded version of the original strings for which hexadecimal values are provided.

```php
<?php

$hex1 = '4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2';
$hex2 = '4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2';

$bin1 = hex2bin($hex1);
$bin2 = hex2bin($hex2);

if ($bin1 == $bin2)
	echo 'The binary data is the same' . PHP_EOL;
else 
	echo 'The binary data is not the same' . PHP_EOL . PHP_EOL;

$md51 = md5($bin1);
$md52 = md5($bin2);

echo 'MD5 hash for binary #1: ' . $md51 . PHP_EOL;
echo 'MD5 hash for binary #2: ' . $md52 . PHP_EOL;

if ($md51 == $md52)
	echo 'The MD5 hashes are the same' . PHP_EOL;
else 
	echo 'The MD5 hashes are not the same' . PHP_EOL;

$urlencoded1 = urlencode($bin1);
$urlencoded2 = urlencode($bin2);
echo PHP_EOL;
echo 'The urlencoded #1 is: '. $urlencoded1 . PHP_EOL;
echo 'The urlencoded #2 is: '. $urlencoded2 . PHP_EOL;
```

The script will give you the strings.

```
The binary data is not the same

MD5 hash for binary #1: 008ee33a9d58b51cfeb425b0959121c9
MD5 hash for binary #2: 008ee33a9d58b51cfeb425b0959121c9
The MD5 hashes are the same

The urlencoded #1 is: M%C9h%FF%0E%E3%5C+%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2
The urlencoded #2 is: M%C9h%FF%0E%E3%5C+%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
```

So you can craft the complete request.

```
GET /?darkctf=2020&ctf2020=WkdGeWEyTjBaaTB5TURJd0xYZGxZZz09&karma=M%C9h%FF%0E%E3%5C+%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2&2020=M%C9h%FF%0E%E3%5C+%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2 HTTP/1.1
Host: php.darkarmy.xyz:7001
User-Agent: 2020_the_best_year_corona
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
```

The webpage will give you the following.

```html
<h1 style='color: chartreuse;'>Flag : DarkCTF{</h1></br><h1 style='color: chartreuse;'>Flag : very_</h1></br><h1 style='color: chartreuse;'>Flag : nice</h1></br><h1 style='color: chartreuse;'>Flag : _web_challenge_dark_ctf}</h1>
```

The flag is the following.

```
DarkCTF{very_nice_web_challenge_dark_ctf}
```