# Evlz CTF 2019 – WeTheUsers

* **Category:** Web
* **Points:** 100

## Challenge

> [http://13.232.233.247:1337/](http://13.232.233.247:1337/)
>
> [https://pastebin.com/VWmk2Jdy](https://pastebin.com/VWmk2Jdy)

## Solution

The [source code](source.py) of the application is given for this challenge.

Analyzing it, you can discover that during user registration data is packed with a format like `username:password:admin`.

The `admin` field can be `true` or `false` and during the normal registration process a `false` value is forced into the ACL.

There are no escaping countermeasures for `:` char, hence a record could be crafted and injected passing a password with that char, in order to bypass the `false` value forced, creating an admin account.

For example, you can use following values during registration:
* username: `m3ssap0`
* password: `pwnd:true`

Logging in with the created user will show the flag:

```
evlz{T#3_W34K_$N4K3}ctf
```