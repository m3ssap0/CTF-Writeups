# Access Denied 1.2 2018 – Monica's fear

* **Category:** web
* **Points:** 150

## Challenge

> Monica figured out Phoebe's grandmother's secret recipe and asked Chandler to hide it somewhere safe. However he was drunk and he can not remember where he kept it.
>
> Can you find it ?
>
> Challenge running at : http://13.58.20.227:8080/

## Solution

In the home page of the website there is a strange message:

> Wow INSTRUO team loves :cookie:

Analyzing browser cookies, you can find the following one:

```
flag : YWNjZXNzZGVuaWVke2MwMGtpM3NfNHIzX3Q0c3R5XzY1OXdkczF9
```

Decoding the Base64 cookie value will give you the flag.

```
accessdenied{c00ki3s_4r3_t4sty_659wds1}
```