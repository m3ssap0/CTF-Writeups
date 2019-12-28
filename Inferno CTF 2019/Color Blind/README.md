# Inferno CTF 2019 – Color Blind

* **Category:** Misc
* **Points:** 139

## Challenge

> What do the colors mean?
>
> Author : nullpxl

## Solution

The challenge gives you [an image](colorblind.png).

![colorblind.png](colorblind.png)

Using *StegOnline* and [extracting data from RGB bits](https://georgeom.net/StegOnline/extract) will give you the following text.

```
blahblahblah_hello_how_are_you_today_i_hope_you_are_not_doing_this_manually_infernoCTF{h3y_100k_y0u_4r3_n07_h3x_bl1nD_:O}_doing_this_manually_would_be_a_bad_idea_you_shouldnt_do_it_manually_ok
```

The flag is the following.

```
infernoCTF{h3y_100k_y0u_4r3_n07_h3x_bl1nD_:O}
```