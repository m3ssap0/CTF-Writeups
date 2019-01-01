# 35C3 Junior CTF – McDonald

* **Category:** Web
* **Points:** 44 (variable)

## Challenge

> Our web admin name's "Mc Donald" and he likes apples and always forgets to throw away his apple cores..
>
> http://35.207.91.38

## Solution

Visiting `http://35.207.91.38/robots.txt` will reveal the following content.

```
User-agent: *
Disallow: /backup/.DS_Store
```

So the `http://35.207.91.38/backup/.DS_Store` will download a `.DS_Store` file.

According to [Wikipedia](https://en.wikipedia.org/wiki/.DS_Store):
> In the Apple macOS operating system, .DS_Store is a file that stores custom attributes of its containing folder, such as the position of icons or the choice of a background image.

The [https://github.com/lijiejie/ds_store_exp](https://github.com/lijiejie/ds_store_exp) script could be used to download and extract hidden data.

```
./ds_store_exp.py http://35.207.91.38/backup/.DS_Store
```

The flag will be into `backup/b/a/c/flag.txt`.

```
35c3_Appl3s_H1dden_F1l3s
```