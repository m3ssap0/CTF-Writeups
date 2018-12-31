# 35C3 Junior CTF – poet

* **Category:** Pwn
* **Points:** variable

## Challenge

> We are looking for the poet of the year:
> 
> nc 35.207.132.47 22223
> 
> Difficulty estimate: very easy

## Solution

The challenge involves a simple *buffer overflow* vulnerability. You will have a binary file only.

The program takes two inputs: a poem and the author's name. Based on the words of the poem, the program calculates a score. Reversing the binary you can see which words give which points, the problem is that a limit on the poem's length will prevent to reach the target score (i.e. exactly 1 million).

Analyzing the binary, you can discover that the flag is contained into a text file printed into `reward` function located at `0x0000000000400767`. The label into the `main` where the flow will jump in case of reward will be at `0x00000000004009f2`, so this could be a good target address where to jump via buffer overflow.

The score is calculated with `rate_poem` function located at `0x00000000004007B7`; this function contains a call to `strcpy`, which is vulnerable to buffer overflow. During normal behavior, the `rate_poem` method will return to `0x00000000004009d8` address in `main`.

The final exploit to overwrite that address will be the following.

```
python -c 'print "A"*1024 ; print "a"*40 + "\xf2\x09\x40\x00\x00\x00\x00\x00"' | nc 35.207.132.47 22223
```

This exploit will print the flag.

```
35C3_f08b903f48608a14cbfbf73c08d7bdd731a87d39
```

## Other solution

It seems that another (intended?) solution was present. It consisted in overwriting the score variable into memory, located after the author's name variable, in order to reach the target score.