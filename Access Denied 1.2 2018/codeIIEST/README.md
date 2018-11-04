# Access Denied 1.2 2018 – codeIIEST

* **Category:** web
* **Points:** 50

## Challenge

> 0xeax developed the codeiiest website and hid the flag somewhere.
>
> It is the most beautiful website I have ever seen on this planet. Why don't you visit the website and get me the flag?
>
> Challenge running at : [https://codeiiest.github.io](https://codeiiest.github.io)

## Solution

In the home page of the website there is the following HTML comment at the end.

```html
<!-- Here's the first part of flag for You.  -->
<!-- part1 
accessdenied{1_w3nt_thr0ug -->

<!-- rest part of flag is in d4rks0c1ety page -->
```

On the other page, i.e. [https://codeiiest.github.io/d4rks0c1ety.html](https://codeiiest.github.io/d4rks0c1ety.html), you can find another HTML comment at the beginning.

```html
<!-- part 2 of the flag is -->
<!-- 
		h_th1s_w3bs1t3} 
-->

<!-- Thanks for your time. -->
```

So the flag is the following:

```
accessdenied{1_w3nt_thr0ugh_th1s_w3bs1t3}
```