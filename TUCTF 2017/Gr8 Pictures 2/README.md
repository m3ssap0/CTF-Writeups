# TUCTF 2017 – Gr8 Pictures 2

* **Category:** misc (stego)
* **Points:** 150

## Challenge

> The mysterious hacker 4chan has switched up his steganography provider! He is now using `gr8pics2.tuctf.com:5555`. Your previous solution will no longer work and his message is a matter of national security. Your mission, agent, is to find out what secrets the mysterious hacker 4chan is hiding in this message from an older version.

```
nc gr8pics2.tuctf.com 5555
```

## Solution

First of all, CRC in the image must be fixed. For example, the following program can be used: [http://schaik.com/png/pngcsum/pngcsum-v01.tar.gz](http://schaik.com/png/pngcsum/pngcsum-v01.tar.gz).

The fixed image can be used to search the original image in the internet. The original image is at: 
[https://vignette.wikia.nocookie.net/ben10/images/4/4c/AaB_%2840%29.png/revision/latest?cb=20150923151143](https://vignette.wikia.nocookie.net/ben10/images/4/4c/AaB_%2840%29.png/revision/latest?cb=20150923151143]).

The original image can be compared with the "flag.png" file using the following command.

```
cmp -l flag.png out.png | gawk '{printf "%08X %02X %02X\n", $1, strtonum(0$2), strtonum(0$3)}'
```

To retrieve the original message, the following operation for each different byte can be performed:

```
original_message = byte_original_message XOR byte_hidden_message
```

The following Java program can be used.

```
package com.tuctf.misc;

public class Misc3 {

    private final static int SECRET[] = { 0xC6, 0x35, 0x96, 0xA0, 0x7C, 0xC1, 0x4E, 0xFB, 0x9E, 0xCD, 0x9A, 0x35, 0xE9, 0x1D, 0x98, 0xA0, 0x4A, 0x3F, 0x73, 0x5E, 0x33, 0x25, 0x13, 0x12, 0xFF, 0x3C, 0x7B, 0x95, 0x52, 0xF8, 0x72, 0xD5, 0xE4, 0xA5, 0x56, 0x7A, 0x55, 0x55, 0x86, 0x59, 0x1D, 0xEC, 0x07, 0x0C, 0x83, 0xBF, 0x22, 0xAB, 0x52, 0x83 };
    private final static int ORIGINAL[] = { 0x92, 0x60, 0xD5, 0xF4, 0x3A, 0xBA, 0x7E, 0x95, 0xAF, 0xB4, 0xC5, 0x04, 0xDA, 0x2E, 0xAF, 0x84, 0x15, 0x5C, 0x33, 0x30, 0x6C, 0x57, 0x20, 0x52, 0x9B, 0x63, 0x16, 0xA6, 0x21, 0x8B, 0x32, 0xB2, 0x81, 0xD6, 0x09, 0x12, 0x3C, 0x31, 0xE2, 0x3C, 0x73, 0xB3, 0x6E, 0x62, 0xDC, 0xFC, 0x70, 0xE8, 0x21, 0xFE };

    public void getFlag() {
        StringBuffer flag = new StringBuffer();

        for (int i = 0; i < SECRET.length; i++) {
            int secretChar = ORIGINAL[i] ^ SECRET[i];
            flag.append((char) secretChar);
        }

        System.out.println("The flag is: " + flag.toString());
    }

    public static void main(String[] args) {
        try {
            Misc3 m = new Misc3();
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
TUCTF{0n1y_1337$_c@n_r3@d_m3ss@ges_hidden_in_CRCs}
```