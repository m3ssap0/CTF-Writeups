# Access Denied 1.2 2018 – GIFer 

* **Category:** forensics
* **Points:** 150

## Challenge

> donfos found a gif file. It looks suspicious. He told you to get the flag quickly and save him.
>
> Can you get the flag for him?
>
> Download file from : [https://accessd.sfo2.digitaloceanspaces.com/foren200.gif](foren200.gif)

## Solution

The file is a GIF image which shows several frames containg parts of the final flag.

![foren200.gif](foren200.gif)

The GIF must be split (e.g. using [https://ezgif.com/split](https://ezgif.com/split)) and then each frame must be merged in the same final image, ignoring white background.

The merge operation can be performed via script or using an image manipulation program (*MS Paint* can be fine).

The final image will be:

![foren200.png](foren200.png)

Hence, the flag is:

```
accessdenied{f0r3ns1cs_1s_s0_c00l}
```