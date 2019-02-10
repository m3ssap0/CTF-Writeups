# Quals Saudi and Oman National Cyber Security CTF 2019 – Hack a nice day

* **Category:** Digital Forensics
* **Points:** 100

## Challenge

> can you get the flag out to hack a nice day. Note: Flag format flag{XXXXXXX}
> 
> [https://s3-eu-west-1.amazonaws.com/hubchallenges/Forensics/info.jpg](https://s3-eu-west-1.amazonaws.com/hubchallenges/Forensics/info.jpg)

## Solution

This is a steganography challenge.

![info.jpg](info.jpg)

Opening the image with an hexadecimal editor will reveal a string at `0x18`: `badisbad`.

Probably something was hidden inside the image with that passphrase. *steghide* can be used to analyze it.

```
$ steghide --info info.jpg
"info.jpg":
  format: jpeg
  capacity: 300.0 Byte
Try to get information about embedded data ? (y/n) y
Enter passphrase: badisbad
  embedded file "flaggg.txt":
    size: 21.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
```

*steghide* can be also used to extract hidden content.

```
$ steghide --extract -sf info.jpg -p badisbad
wrote extracted data to "flaggg.txt".
```

The file contains the flag.

```
flag{Stegn0_1s_n!ce}
```