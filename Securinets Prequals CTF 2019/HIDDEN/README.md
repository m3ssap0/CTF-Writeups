# Securinets Prequals CTF 2019 – HIDDEN

* **Category:** Misc
* **Points:** 200

## Challenge

> My friend asked me to find his hidden flag in this link .. Can you help me?
>
> https://misc1.ctfsecurinets.com/
>
> Author:Tr'GFx

## Solution

Connecting to the website you will experience a trusting error on the HTTPS certificate.

The website will only print a message: `Flag is somewhere here`.

Examining the certificate, you will find the flag into the issuer information.

```
E = challenge@securinets.com
CN = ctfsecurinets.com
O = Securinets{HiDDeN_D@tA_In_S3lF_S3iGnEd_CeRtifICates}
L = Tunis
S = Tunisia
C = TN
```

The flag is the following.

```
Securinets{HiDDeN_D@tA_In_S3lF_S3iGnEd_CeRtifICates}
```