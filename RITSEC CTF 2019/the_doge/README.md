# RITSEC CTF 2019 – the_doge

* **Category:** stego
* **Points:** 100

## Challenge

> Steganography is the practice of concealing messages or information within other nonsecret data and images. The doge holds the information you want, feed the doge a treat to get the hidden message.
>
> Author: adriannav

## Solution

The challenge gives you an [image](the_doge.jpg). 

[the_doge.jpg](the_doge.jpg)

The text says that you have to *feed the doge a **treat** to get the hidden message*, so probably something is hidden inside the image with *treat* used like a passphrase.

You can use *steghide* to discover the presence of [doge_ctf.txt](doge_ctf.txt) hidden file.

```
root@m3ss4p0:~# steghide info the_doge.jpg
"the_doge.jpg":
  format: jpeg
  capacity: 1,1 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: treat
  embedded file "doge_ctf.txt":
    size: 23,0 Byte
    encrypted: no
    compressed: no
root@m3ss4p0:~# steghide extract -sf the_doge.jpg
Enter passphrase: treat
wrote extracted data to "doge_ctf.txt".
root@m3ss4p0:~# cat doge_ctf.txt 
RITSEC{hAppY_l1L_doG3}
```

The flag is the following.
```
RITSEC{hAppY_l1L_doG3}
```