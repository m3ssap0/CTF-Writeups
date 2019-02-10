# Quals Saudi and Oman National Cyber Security CTF 2019 – I love images

* **Category:** Digital Forensics
* **Points:** 50

## Challenge

> A hacker left us something that allows us to track him in this image, can you find it?
> 
> [https://s3-eu-west-1.amazonaws.com/hubchallenges/Forensics/godot.png](https://s3-eu-west-1.amazonaws.com/hubchallenges/Forensics/godot.png)

## Solution

This is a steganography challenge.

![godot.png](godot.png)

Opening the image with an hexadecimal editor will reveal a strange content at the end.

```
IZGECR33JZXXIX2PNZWHSX2CMFZWKNRUPU======
```

The string is encoded in base32, decoding it will reveal the flag.

```
FLAG{Not_Only_Base64}
```