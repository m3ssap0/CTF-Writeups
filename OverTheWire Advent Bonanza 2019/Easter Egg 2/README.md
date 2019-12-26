# OverTheWire Advent Bonanza 2019 – Easter Egg 2

* **Category:** fun
* **Points:** 10

## Challenge

> Easter Egg 2
>
> Service: https://advent2019.overthewire.org
> 
> Author: EasterBunny

## Solution

Opening a challenge modal window, you can find a strange response HTTP header returned when `https://advent2019.overthewire.org/static/fonts/roboto/Roboto-Bold.woff2` file is downloaded.

![EasterEgg2.png](EasterEgg2.png)

```
x-easteregg2: ==QftRHdz8VZydmZuNzXhJ3MxcGMltnSHJkT
```

Reversing the string.

```
TkJHSntlMGcxM3JhXzNuZmdyZV8zdHRtfQ==
```

Base64 decoding.

```
NBGJ{e0g13ra_3nfgre_3ttm}
```

Using ROT13.

```
AOTW{r0t13en_3aster_3ggz}
```