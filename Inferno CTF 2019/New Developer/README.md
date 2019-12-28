# Inferno CTF 2019 – New Developer

* **Category:** OSINT
* **Points:** 50

## Challenge

> A friend of a friend of a friend who is known for leaking info was recently hired at a game company. What can you find in their GitHub profile?
> 
> https://github.com/iamthedeveloper123
>
> Author: nullpxl

## Solution

Analyzing the commits of one of its projects on Github, you can find the following.

```
https://github.com/iamthedeveloper123/bash2048/commit/f6008f3d67829ad0ab19d029eec6833a196db8d8
```

It contains an interesting change.

```bash
printf "\nYou have lost, try going to https://pastebin.com/$CODE for help!.  (And also for some secrets...) \033[0m\n"
```

The content of the environment variable `$CODE` can be found inside a dot file.

```
https://github.com/iamthedeveloper123/dotfiles/blob/master/.bashrc2#L83
```

The value is the following.

```bash
export CODE="trpNwEPT"
```

So connecting to `https://pastebin.com/trpNwEPT` will give you the flag.

```
infernoCTF{n3ver_4dd_sen5itv3_7hings_to_y0ur_publ1c_git}
```