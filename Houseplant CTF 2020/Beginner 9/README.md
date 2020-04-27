# Houseplant CTF 2020 – Beginner 9

* **Category:** beginners, crypto
* **Points:** 25

## Challenge

> Hope you've been paying attention! :D
> 
> Remember to wrap the flag with rtcp{}
>
> Hint! we stan cyberchef in this household
>
> Beginner 10.txt 200e8ed3c39c36c1c9a2ff2a87a5f5d8

## Solution

The challenge gives you [a file](Beginner10.txt) with the following content. Multiple encoding/encryption algorithms are used.

```
MmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMGEgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmQgMmQgMmQgMmQgMmQgMjAgMmUgMmQgMmQgMmQgMmQ=
```

From base64 you will have the following.

```
2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 0a 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2e 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2d 2d 2d 2d 2d 20 2e 2d 2d 2d 2d
```

From hexadecimal representation you will have the following.

```
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- .---- -----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- .---- ----- .----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- .---- -----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- .---- ----- ----- .----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- ----- .----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- .---- -----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- ----- .----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- ----- ----- .---- -----
----- ----- .---- .---- ----- .---- .---- -----
----- ----- .---- ----- ----- ----- ----- -----
----- ----- .---- .---- .---- ----- ----- .----
```

From Morse code you will have the following.

```
00110010 00110110 00100000 00110101 00100000 00110010 00110110 00100000 00111001 00100000 00110010 00110101 00100000 00110010 00110010 00100000 00110010 00110110 00100000 00110010 00110101 00100000 00110010 00110110 00100000 00111001
```

From binary representation you will have the following.

```
26 5 26 9 25 22 26 25 26 9
```

From A1Z26 cipher you will have the following.

```
zeziyvzyzi
```

From ROT13 you will have the following.

```
mrmvlimlmv
```

From Atbash cipher you will have the following.

```
nineornone
```

So the flag is the following.

```
rtcp{nineornone}
```