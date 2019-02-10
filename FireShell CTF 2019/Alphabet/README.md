# FireShell CTF – Alphabet

* **Category:** crypto
* **Points:** 60

## Challenge

> If you know your keyboard, you know the flag

## Solution

The challenge provides a file with several strings in it: [submit_the_flag_that_is_here.txt](submit_the_flag_that_is_here.txt).

Based on their dimensions (i.e. 32 chars and 64 chars), strings seem to be MD5 and SHA-256 hashes.

Considering the text of the challenge, they could be hashes of keyboard chars; hence it is sufficient to produce MD5 and SHA-256 dictionaries to reverse the hashes.

Following Python script could be used.

```python
import hashlib

print "[*] Creating dictionaries."
dictionary_md5 = {}
dictionary_sha256 = {}
for i in range(32, 127):
   plain_char = chr(i)
   print "[*] Hashing char: {}".format(plain_char)
   dictionary_md5[hashlib.md5(plain_char).hexdigest()] = plain_char
   dictionary_sha256[hashlib.sha256(plain_char).hexdigest()] = plain_char

print "[*] Reading file."
with file("submit_the_flag_that_is_here.txt") as f:
   file_content = f.read()
hashed_chars = file_content.split(" ");

print "[*] Decrypting message."
decrypted_message = ""
for h in hashed_chars:
   
   decrypted_char = None
   if len(h) == 32:
      decrypted_char = dictionary_md5[h]
   elif len(h) == 64:
      decrypted_char = dictionary_sha256[h]
   
   if decrypted_char is not None:
      decrypted_message += decrypted_char

print "[*] Decrypted message:"
print decrypted_message
```

It will reveal the message with the flag.

```
Congratulations!_T#e_Flag_Is_F#{Y3aH_Y0u_kN0w_mD5_4Nd_Sh4256}
```