# Access Denied 1.2 2018 – Shalias 

* **Category:** misc
* **Points:** 150

## Challenge

> I've written a the flag into flag.txt. However, someone under the alias of donfus messed the terminal up. Can you help me find the flag?
> Challenge running at :
> ssh user@139.59.37.86 -p 4849
> password is : accessd
> (You need a SSH client)

## Solution

The `flag.txt` file is in the home diractory of the user, but the `cat` command seems to not work.

Analyzing the `/bin/` directory will reveal that the `cat` command exists, hopefully.

```
user@78718481b4f8:~$ ls /bin/
```

It can be used to print the flag.

```
user@78718481b4f8:~$ /bin/cat flag.txt
accessdenied{un4li4sing_w4s_34sy_5994asd}
```