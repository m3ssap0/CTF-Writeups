# Securinets Prequals CTF 2019 – Easy Trade

* **Category:** Foren
* **Points:** 200

## Challenge

> We just intercepted some newbies trying to trade flags.
>
> [foren_trade.pcap](foren_trade.pcap)
>
> Author: bibiwars

## Solution

The [pcap file](foren_trade.pcap) contains a capture with a conversation between two people during which an archive file was trasferred.

The transfer was performed at packet #23.

The data can be copied and put into a file using an hexadecimal editor.

```
50 4b 03 04 0a 00 09 00 00 00 6e 80 77 4e 20 64 e5 de 48 00 00 00 3c 00 00 00 08 00 1c 00 66 6c 61 67 2e 74 78 74 55 54 09 00 03 c0 4a 96 5c c0 4a 96 5c 75 78 0b 00 01 04 e8 03 00 00 04 e8 03 00 00 1c 07 86 f2 a0 ac 34 d9 93 33 f0 b9 19 2d cb b4 74 5e fd 2f e4 5b 7d b5 33 f0 0a d8 9b 75 12 b8 21 3a 65 f9 5e 82 7b e6 c2 63 8f ac 42 c4 a1 33 bb 22 d5 e9 2a 95 8a 18 3e bd ae 0c a3 9b 3b fc e5 c4 6b 5d 96 88 3b 5c 50 4b 07 08 20 64 e5 de 48 00 00 00 3c 00 00 00 50 4b 01 02 1e 03 0a 00 09 00 00 00 6e 80 77 4e 20 64 e5 de 48 00 00 00 3c 00 00 00 08 00 18 00 00 00 00 00 01 00 00 00 b4 81 00 00 00 00 66 6c 61 67 2e 74 78 74 55 54 05 00 03 c0 4a 96 5c 75 78 0b 00 01 04 e8 03 00 00 04 e8 03 00 00 50 4b 05 06 00 00 00 00 01 00 01 00 4e 00 00 00 9a 00 00 00 00 00 
```

The [resulting zip file](flag.zip) is protected and the password to open it is `securinetsXD`; you can read it in packet #13.

The file contains the following string.

```
c2VjdXJpbmV0c3s5NTRmNjcwY2IyOTFlYzI3NmIxYTlmZjg0NTNlYTYwMX0
```

Decoding the base64, you will obtain the flag.

```
securinets{954f670cb291ec276b1a9ff8453ea601}
```