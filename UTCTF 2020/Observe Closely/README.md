# UTCTF 2020 – Observe Closely

* **Category:** forensics
* **Points:** 50

## Challenge

> A simple image with a couple of twists...
> 
> by phleisch

## Solution

The challenge gives you [an image](Griffith_Observatory.png).

![Griffith_Observatory.png](Griffith_Observatory.png)

Analyzing the image with an hexeditor, you can discover an hidden archive appended, because you can spot a `PK` file signature at the end of the file.

In the archive, an [hidden ELF file](hidden_binary) can be found.

It is sufficient to run the executable to get the flag.

```
root@m3ss4p0:~/Desktop# chmod u+x hidden_binary 
root@m3ss4p0:~/Desktop# ./hidden_binary 
Ah, you found me!
utflag{2fbe9adc2ad89c71da48cabe90a121c0}
```