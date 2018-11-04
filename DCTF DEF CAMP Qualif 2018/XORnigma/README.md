# DCTF DEF CAMP Qualif 2018 – XORnigma

* **Category:** crypto
* **Points:** 1

## Challenge

> Obtain the flag from the given [file](xornigma.py).

## Solution

The given file contains a cipher algorithm and the resulting ciphertext. The ciphertext is:

```
000000003f2537257777312725266c24207062777027307574706672217a67747374642577263077777a3725762067747173377326716371272165722122677522746327743e
```

The algorithm is a simple XOR cipher that can be inverted on the ciphertext using the same `flag_key`.

The ciphertext begins with `00000000`, so `flag` and `flag_key` have the same first 4 bytes. Considering the standard format of flags, `flag_key` could be `DCTF`.

So the script can be changed as the following:

```python
import itertools
def xor_two_str(s, key):
	key = key * (len(s) / len(key) + 1)
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(s, key)) 

flag = "" 
flag_key = "DCTF"
x_dec = "000000003f2537257777312725266c24207062777027307574706672217a67747374642577263077777a3725762067747173377326716371272165722122677522746327743e".decode("hex")
flag = xor_two_str(x_dec, flag_key)
print flag
```

And it will print the flag:

```
DCTF{fcc34eaae8bd3614dd30324e932770c3ed139cc2c3250c5b277cb14ea33f77a0}
```