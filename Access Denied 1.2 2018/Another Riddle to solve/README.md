# Access Denied 1.2 2018 – Another Riddle to solve

* **Category:** crypto
* **Points:** 150

## Challenge

> Francis Bacon once told me "I have your flag. Ask me nicely and I shall give you the flag."
> Download file from : [https://accessd.sfo2.digitaloceanspaces.com/crypto150.txt](https://accessd.sfo2.digitaloceanspaces.com/crypto150.txt)

## Solution

Considering the quote of Francis Bacon, the [Bacon's cipher](https://en.wikipedia.org/wiki/Bacon%27s_cipher) must be involved.

The content of the downloaded file is the following:

```
QUFBQUFBQUFCQUFBQUJBQUFCQUFCQUFBQkJBQUFCQUFBQkJBQUJBQUFCQkFBQUJBQUFBQUJBQUFBQUJCQUFBQkJBQUJBQUFCQUJBQUJBQUFBQXtBQkFBQkFBQUFCQkFCQkFBQkJCQUFBQkFBQUFCQUFBQUFBQUFCQUFCQkFCQUJCQUFBQUFCQkFBQkFBQUJBQkFBQkFBQUFBQUJBQUJBQUFBQkJBQkJBQUJCQkFBQUJBQkJCQUFCQkFCQUJBQUFBQkJBQUJBQUJBQkFBQUJ9
```

But it doesn't seem a text encoded with Bacon's cipher. It is a Base64 encoded text, so the first step is to decode it.

```
AAAAAAAABAAAABAAABAABAAABBAAABAAABBAABAAABBAAABAAAAABAAAAABBAAABBAABAAABABAABAAAAA{ABAABAAAABBABBAABBBAAABAAAABAAAAAAAABAABBABABBAAAAABBAABAAABABAABAAAAAABAABAAAABBABBAABBBAAABABBBAABBABABAAAABBAABAABABAAAB}
```

Now the text can be decoded using an [on-line tool](https://www.dcode.fr/bacon-cipher).

The flag is:

```
ACCESSDENIED{DELICIOUSBACONDELICIOUSPOINTS}
```