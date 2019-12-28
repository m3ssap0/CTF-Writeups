# Inferno CTF – Wannabe Rapper

* **Category:** Reversing
* **Points:** 197

## Challenge

> An Android Pentester and Wannabe Rapper extracted the following files from an app.
> 
> PS: He loves Eminem!!
> 
> flag : infernoCTF{username:password}
> 
> Author : MrT4ntr4

## Solution

The challenge gives you [an archive](wannabe_rapper.zip) with three files:
* [`MainActivity$1.smali`](wannabe_rapper/MainActivity$1.smali);
* [`MainActivity$2.smali`](wannabe_rapper/MainActivity$2.smali);
* [`MainActivity.smali`](wannabe_rapper/MainActivity.smali).

These files are extracted from an Android application and you have to find a username and a password.

Analyzing the [`MainActivity$1.smali`](wannabe_rapper/MainActivity$1.smali), you can notice a curious constant that can be related to Eminem.

```
.line 70
const-string v1, "m&m"
```

So the username could be `m&m`.

You can find another interesting snippet into [`MainActivity.smali`](wannabe_rapper/MainActivity.smali), in the constructor.

```
# direct methods
.method public constructor <init>()V
    .registers 5

    .line 14
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 19
    const/4 v0, 0x3

    iput v0, p0, LMainActivity;->counter:I

    .line 21
    const/16 v1, 0x8

    new-array v1, v1, [Ljava/lang/String;

    const-string v2, "84"

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "5"

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "2"

    const/4 v3, 0x2

    aput-object v2, v1, v3

    const-string v2, "f8eb53473"

    aput-object v2, v1, v0

    const-string v0, "4"

    const/4 v2, 0x4

    aput-object v0, v1, v2

    const-string v0, "2efb3d"

    const/4 v2, 0x5

    aput-object v0, v1, v2

    const-string v0, "f"

    const/4 v2, 0x6

    aput-object v0, v1, v2

    const-string v0, "82df"

    const/4 v2, 0x7

    aput-object v0, v1, v2

    invoke-static {v1}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->lol:Ljava/util/List;

    .line 22
    const-string v0, "a"

    iget-object v1, p0, LMainActivity;->lol:Ljava/util/List;

    invoke-static {v0, v1}, Ljava/lang/String;->join(Ljava/lang/CharSequence;Ljava/lang/Iterable;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->magic:Ljava/lang/String;

    .line 23
    iget-object v0, p0, LMainActivity;->magic:Ljava/lang/String;

    const-string v1, "8"

    const-string v2, "0"

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->secret:Ljava/lang/String;

    return-void
.end method
```

In this code, some values are inserted into an array.

```
84     5      2      f8eb53473  4      2efb3d  f      82df
^.0x0  ^.0x1  ^.0x2  ^.0x3      ^.0x4  ^.0x5   ^.0x6  ^.0x7
```

The array is converted into a list. Then a `join` method is invoked using `a` char as separator. The result is the following.

```
84a5a2af8eb53473a4a2efb3dafa82df
```

At this point, a `replaceAll` method is invoked, replacing all `8` chars with `0` chars. The result is the following.

```
04a5a2af0eb53473a4a2efb3dafa02df
```

Considering that in the source code there is a method called `md5`, this could be a MD5 hash. Trying to crack it, you will discover that this is the MD5 of the string `mockingbird78209`.

One of Eminem's song is called [Mockingbird](https://www.youtube.com/watch?v=S9bCLPwzSC0), so this string could be the password.

The complete flag is the following.

```
infernoCTF{m&m:mockingbird78209}
```