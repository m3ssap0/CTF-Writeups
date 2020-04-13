# DawgCTF 2020 – Where did the spaces go?

* **Category:** misc
* **Points:** 100

## Challenge

> -.--.---...--....-.--...-.-----..-...--.---..--...-.--...-...-..-......----..-...-........--.-.-..--..-...-..-......----...--..-...-..-.....-.-.---.-.----.
> 
> Note: this one is /slightly/ out of flag format, but it's still very clear when you get it. Flag will be accepted as it is, or altered to fit in format.
> 
> author: pleoxconfusa

## Solution

The reported code is not Morse; a Morse code without spaces is very difficult to crack and analyzing that code you can discover that Morse representation of `DAWGCTF` string is completely absent.

Some telegraph codes have fixed length representation for each char, one of them is *Baudot*, with chars represented by 5 binary numbers each.

The given string is 155 chars long, so it is sufficient to convert the original string into binary.

```
-.--.---...--....-.--...-.-----..-...--.---..--...-.--...-...-..-......----..-...-........--.-.-..--..-...-..-......----...--..-...-..-.....-.-.---.-.----.

01001000111001111010011101000001101110010001100111010011101110110111111000011011101111111100101011001101110110111111000011100110111011011111010100010100001
```

Then to use this [Baudot code decoder online](https://www.dcode.fr/baudot-code) to obtain the flag.

```
DAWGCTFBAUD0T1SN0TM0RSE
```