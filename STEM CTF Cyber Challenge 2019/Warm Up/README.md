# STEM CTF Cyber Challenge 2019 – Warm Up

* **Category:** Crypto
* **Points:** 50

## Challenge

> Everyone says that PGP is hard to use. Show ‘em how it’s done.

## Solution

The challege gives you [some files](warm-up.zip).

The first step is to import the secret key.

```
$ gpg --allow-secret-key-import --import mitre-ctf-2019-private.asc
gpg: key D70E64BECB374E23: "CTF Competitor (This is private key for a 2019 MITRE CTF Competitor and should not be trusted!) <fake@fake>" not changed
gpg: key D70E64BECB374E23: secret key imported
gpg: Total number processed: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:  secret keys unchanged: 1
```

Then, using the passphrase into `passphrase.txt` file: `just use ctfd`, decrypt the `key.enc` file.

```
$ gpg --output key --decrypt key.enc
gpg: encrypted with 2048-bit RSA key, ID 2D312D1F87BA2B5E, created 2018-12-03
      "CTF Competitor (This is private key for a 2019 MITRE CTF Competitor and should not be trusted!) <fake@fake>"
gpg: Signature made lun 03 dic 2018 23:48:09 CET
gpg:                using RSA key 587735E31F0B06751ACD0D53CDE38825F2FFFCB4
gpg: Can't check signature: No public key
```

The `flag.html.enc` file is salted and encrypted with OpenSSL.

```
$ binwalk flag.html.enc

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             OpenSSL encryption, salted, salt: 0xF61A179-5D7CAE48
```

The following OpenSSL command can be used to decrypt it.

```
$ openssl aes-256-cbc -kfile key -d -in flag.html.enc -out flag.html -md md5
```

The decrypted file contains a false flag and a real one hidden.

```
$ more flag.html
<!DOCTYPE html>
<html>
<head>
  <title>MITRE CTF 2019 Homepage.</title>
</head>
<body>
<h1>This is an HTML Page</h1>
<br>
<p>Test Flag please ignore:</p>
<p>MCA{0p3n55l_c0mm4nd_l1ne_ch4ll3ng3_fl4g}</p>
<p style="display:none;">MCA{66b2f50cd2d6b9622c6be902ee2b0976badb4684}</p>
</body>
</html>
```

The flag is the following.

```
MCA{66b2f50cd2d6b9622c6be902ee2b0976badb4684}
```