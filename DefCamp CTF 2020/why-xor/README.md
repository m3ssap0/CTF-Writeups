# DefCamp CTF 2020 – why-xor

* **Category:** cryptography
* **Points:** 50

## Challenge

> Let's be fair, we all start with XOR, and we keep enjoying it.
> 
> Flag format: CTF{sha256}
> 
> The challenge was proposed by BIT SENTINEL.

## Solution

The challenge gives you [a Python script](xor.py).

```python
xored = ['\x00', '\x00', '\x00', '\x18', 'C', '_', '\x05', 'E', 'V', 'T', 'F', 'U', 'R', 'B', '_', 'U', 'G', '_', 'V', '\x17', 'V', 'S', '@', '\x03', '[', 'C', '\x02', '\x07', 'C', 'Q', 'S', 'M', '\x02', 'P', 'M', '_', 'S', '\x12', 'V', '\x07', 'B', 'V', 'Q', '\x15', 'S', 'T', '\x11', '_', '\x05', 'A', 'P', '\x02', '\x17', 'R', 'Q', 'L', '\x04', 'P', 'E', 'W', 'P', 'L', '\x04', '\x07', '\x15', 'T', 'V', 'L', '\x1b']
s1 = ""
s2 = ""
# ['\x00', '\x00', '\x00'] at start of xored is the best hint you get
a_list = [chr(ord(a) ^ ord(b)) for a,b in zip(s1, s2)]
print(a_list)
print("".join(a_list))
```

The comment in the script is a hint: secret could be composed by a sequence of `ctf` strings and this explains why first 3 chars are zeros (i.e. `'ctf' ^ 'ctf'`).

Another [Python script](why-xor.py) can be implemented to reverse the original script.

```python
xored = ['\x00', '\x00', '\x00', '\x18', 'C', '_', '\x05', 'E', 'V', 'T', 'F', 'U', 'R', 'B', '_', 'U', 'G', '_', 'V', '\x17', 'V', 'S', '@', '\x03', '[', 'C', '\x02', '\x07', 'C', 'Q', 'S', 'M', '\x02', 'P', 'M', '_', 'S', '\x12', 'V', '\x07', 'B', 'V', 'Q', '\x15', 'S', 'T', '\x11', '_', '\x05', 'A', 'P', '\x02', '\x17', 'R', 'Q', 'L', '\x04', 'P', 'E', 'W', 'P', 'L', '\x04', '\x07', '\x15', 'T', 'V', 'L', '\x1b']
secret = "ctf" * len(xored)
a_list = [chr(ord(a) ^ ord(b)) for a,b in zip(xored, secret)]
print("".join(a_list))
```

The flag is the following.

```
ctf{79f107231696395c004e87dd7709d3990f0d602a57e9f56ac428b31138bda258}
```