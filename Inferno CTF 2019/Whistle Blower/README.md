# Inferno CTF 2019 – Whistle Blower

* **Category:** OSINT
* **Points:** 226

## Challenge

> After playing some 2048 you come across an interesting email exchange... What could it lead to?
> 
> Author : nullpxl

## Solution

The challenge gives you [an e-mail exchange log](employment_status.mbox).

In the last e-mail, *imdeveloper123* talks about Twitter.

> Hope you like being the center of attention on infosec twitter!

On Twitter you can find his account: `https://twitter.com/imdeveloper123`. There are two tweets talking about a deleted website.

![tweet.png](tweet.png)

The URL was: `iamthedeveloper123.weebly.com`.

You can use the [Wayback Machine](https://web.archive.org/) to find a snapshot of the website.

```
https://web.archive.org/web/20191224223734/https://iamthedeveloper123.weebly.com/
```

The snapshot contains the flag.

```
infernoCTF{y0u_f0und_7h3_d1sgrun7l3d_empl0y33!}
```