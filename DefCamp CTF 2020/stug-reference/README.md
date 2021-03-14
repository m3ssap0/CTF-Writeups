# DefCamp CTF 2020 – stug-reference

* **Category:** steganography
* **Points:** 50

## Challenge

> Do you have your own stug pass hidden within?
> 
> Flag format: ctf{sha256}
> 
> The challenge was proposed by BIT SENTINEL.


## Solution

The challenge gives you [an image](stug.jpg).

![stug.jpg](stug.jpg)

The text in the image seems a hint to [*Steghide* tool](http://steghide.sourceforge.net/).

```
root@m3ss4p0:~/Scrivania# steghide extract -sf stug.jpg
Enter passphrase: stug
wrote extracted data to "flag.txt".
root@m3ss4p0:~/Scrivania# more flag.txt 
ctf{32849dd9d7e7b313c214a7b1d004b776b4af0cedd9730e6ca05ef725a18e38e1}
```