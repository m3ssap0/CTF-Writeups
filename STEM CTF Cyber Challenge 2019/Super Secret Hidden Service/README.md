# STEM CTF Cyber Challenge 2019 – Super Secret Hidden Service

* **Category:** Web
* **Points:** 50

## Challenge

> https://138.247.13.115

## Solution

Connecting to the website the following message is prompted.

```
421 Site 138.247.13.115 is not served on this interface
```

The website is under HTTPS, but the certificate seems invalid. Analyzing the certificate, you will discover that it was created for the host `138.247.13.115.xip.io`.

Connecting to `https://138.247.13.115.xip.io/` will print the flag.

```
MCA{shuHeimoowaiF5a}
```