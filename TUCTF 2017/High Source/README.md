# TUCTF 2017 – High Source

* **Category:** web
* **Points:** 25

## Challenge

> This guy is getting wayyy too full of himself. He's called himself a master programmer, and he believes he has written a secure login function. Knock him off his high source.
>
> [http://highsource.tuctf.com/](http://highsource.tuctf.com/)

## Solution

The login is performed via a JavaScript script (i.e. `scripts/login.js)`.

Analyzing the code you can see the password that should be used to login:

```
I4m4M4st3rC0d3rH4x0rsB3w43
```

Using that password, you can find the flag:

```
TUCTF{H1gh_S0urc3_3qu4ls_L0ng_F4ll}
```