# DCTF DEF CAMP Qualif 2018 – Multiple Flags

* **Category:** stego
* **Points:** 1

## Challenge

> Look, flags everywhere!
>
> ![multiple-flags.png](multiple-flags.png)

## Solution

The given image contains [flag semaphore](https://en.wikipedia.org/wiki/Flag_semaphore) characters.

They can be decoded considering that:
* `J` could mean "letters from now on" (for the sake of simplicity the `"` char will be used below);
* `#` means "numbers from now on".

So the message is:

```
"DCTFSP
ECIALFL
AG#00"A
A#00"AA
#009913
37"DCTF
```

Giving the following flag:

```
DCTFSPECIALFLAG00AA00AA00991337DCTF
```