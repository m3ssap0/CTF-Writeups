# AUCTF 2020 – Manager

* **Category:** password cracking
* **Points:** 760

## Challenge

> There might be a flag inside this file. The password is all digits.
> 
> NOTE: The flag is NOT in the standard auctf{} format
> 
> Author: OG_Commando

## Solution

The challenge gives you a [KeePass archive](manager.kdbx).

You can use John the Ripper to produce the [hash](manager.hash) and to crack it.

```
root@m3ss4p0:~# keepass2john manager.kdbx > manager.hash
root@m3ss4p0:~# cat manager.hash 
manager:$keepass$*2*60000*0*f31bf71589af9d69d3a9d58b97755405de93aedfbefe244129bb5ac64ed8af41*2f0e592de948bbc65eb9738af2daca231ae54c851ceb1e98f16a69e8f5f48336*8a868c9aedf169c857a8734188bba8eb*8f12fb161ef9e102ef805b84f5ee733c2a645b71099cbf8dab1ed750c58756ee*34fe5cf5eb7991a826a71c3330f88ce9c5ed7cf0e041e4e50a24110d2a69cdd7
root@m3ss4p0:~# john --format:keepass --incremental=digits manager.hash 
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 60000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES, 1=TwoFish, 2=ChaCha]) is 0 for all loaded hashes
Press 'q' or Ctrl-C to abort, almost any other key for status
157865           (manager)
1g 0:03:31:46 DONE (2020-04-05 04:48) 0.000078g/s 88.74p/s 88.74c/s 88.74C/s 157865
Use the "--show" option to display all of the cracked passwords reliably
Session completed
root@m3ss4p0:~# john --show manager.hash
manager:157865

1 password hash cracked, 0 left
```

The flag into the KeePass archive is the following.

```
y0u4r34r34lh4ck3rn0w#!$1678
```