# TUCTF 2017 – Gr8 Pictures

* **Category:** misc (stego)
* **Points:** 50

## Challenge

> The mysterious hacker 4chan is believed to be passing secret messages hidden in a picture. We know that he connects to `gr8pics.tuctf.com:4444` to hide his message in the picture. Your mission, should you choose to accept it, is to find out what message he is trying to hide.

```
nc gr8pics.tuctf.com 4444
```

## Solution

After sending a 50 char string to the endpoint, an image encoded in Base64 is returned. With the following command the real image can be retrieved.

```
python -c 'print "A"*49' | nc -vvv gr8pics.tuctf.com 4444 | base64 -d > out.png
```

This image can be compared to the "flag.png" one. 50 bytes are different. It seems that content of the bytes is garbage, but probably because message chars are XOR-ed with the image bytes.

```
cmp -l flag.png out.png | gawk '{printf "%08X %02X %02X\n", $1, strtonum(0$2), strtonum(0$3)}'
```

To retrieve the original message, the following operation for each different byte can be performed:

```
original_message = (byte_my_message XOR byte_letter_A) XOR byte_hidden_message
```

Warning: the last byte is XOR-ed with string termination char!

The following Java program can be used.

```java
package com.tuctf.misc;

public class Misc2 {

    private final static int SECRET[] = { 0x1D, 0x26, 0x2D, 0x20, 0x19, 0x03, 0x43, 0x06, 0x6C, 0x14, 0x35, 0x0D, 0x58, 0x38, 0x32, 0x1F, 0x13, 0x58, 0x49, 0x4B, 0x2C, 0x39, 0x06, 0x01, 0x3C, 0x17, 0x59, 0x5F, 0x02, 0x13, 0x07, 0x02, 0x6F, 0x1D, 0x10, 0x3C, 0x1B, 0x2B, 0x04, 0x3E, 0x5D, 0x40, 0x6C, 0x5A, 0x26, 0x37, 0x0C, 0x0B, 0x57, 0x0F };
    private final static int MINE[] = { 0x08, 0x32, 0x2F, 0x35, 0x1E, 0x39, 0x71, 0x33, 0x1E, 0x32, 0x34, 0x22, 0x29, 0x1E, 0x01, 0x1E, 0x22, 0x71, 0x71, 0x2D, 0x1E, 0x27, 0x34, 0x2F, 0x22, 0x35, 0x28, 0x2E, 0x2F, 0x7E, 0x08, 0x2C, 0x1E, 0x32, 0x34, 0x22, 0x29, 0x1E, 0x20, 0x1E, 0x70, 0x72, 0x72, 0x76, 0x1E, 0x29, 0x20, 0x39, 0x71, 0x33 };

    public void getFlag() {
        StringBuffer flag = new StringBuffer();

        for (int i = 0; i < SECRET.length; i++) {
            int secretChar = (MINE[i] ^ 'A') ^ SECRET[i];
            flag.append((char) secretChar);
        }

        System.out.println("The flag is: " + flag.toString());
    }

    public static void main(String[] args) {
        try {
            Misc2 m = new Misc2();
            m.getFlag();
        } catch (Exception e) {
            System.err.println("Unexpected error!");
            e.printStackTrace();
        }
    }
}
```

The flag is:

```
TUCTF{st3g@n0gr@phy's_so_c00l,No0ne_steals_my_msg}
```