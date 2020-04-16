# DawgCTF 2020 – ClearEdge Challenges: The Lady is a Smuggler + Let Her Eat Cake! + Tracking

These are multiple challenges connected together.

The website is at: https://clearedge.ctf.umbccd.io/

The HTML of the page is the following.

```html
<!DOCTYPE html>
<html lang="en-US">
<head>
  <img src="https://raw.githubusercontent.com/UMBCCyberDawgs/umbccyberdawgs.github.io/master/images/avatar-cyberdefense-locked.png">
</head>

<body>

  <img src=".." height="1px" width="1px" onclick="alert(String.fromCharCode(68,97,119,103,67,84,70,123,67,108,101,97,114,69,100,103,101,95,117,110,105,125))" >

  <img src="https://media.defense.gov/2018/Sep/03/2001961221/400/400/0/180903-D-IM742-2028.JPG?flag=DawgCTF{ClearEdge_ElizebethSmith)">
  <p>
    America's first female cryptanalyst, she said: "Our office doesn't make 'em, we only break 'em".  On this day, let her eat cake!
  </p>

  <code>  Hwyjpgxwkmgvbxaqgzcsnmaknbjktpxyezcrmlja?</code>

  <p></p>
  <code>  GqxkiqvcbwvzmmxhspcsqwxyhqentihuLivnfzaknagxfxnctLcchKCH{CtggsMmie_kteqbx}</code>


</body>
</html>
```

## The Lady is a Smuggler

* **Category:** web/networking
* **Points:** 25

### Challenge

> Our mysterious lady is smuggling a bit of extra information.
> 
> https://clearedge.ctf.umbccd.io/
> 
> Author: ClearEdge

### Solution

The interesting part is the following.

```html
<img src="https://media.defense.gov/2018/Sep/03/2001961221/400/400/0/180903-D-IM742-2028.JPG?flag=DawgCTF{ClearEdge_ElizebethSmith)">
```

The flag is the following.

```
DawgCTF{ClearEdge_ElizebethSmith}
```

## Let Her Eat Cake!

* **Category:** misc
* **Points:** 75

### Challenge

> She's hungry!
> 
> https://clearedge.ctf.umbccd.io/
> 
> Author: ClearEdge

### Solution

The web page contains the following encrypted message.

```
Hwyjpgxwkmgvbxaqgzcsnmaknbjktpxyezcrmlja?
GqxkiqvcbwvzmmxhspcsqwxyhqentihuLivnfzaknagxfxnctLcchKCH{CtggsMmie_kteqbx}
```

The message is encrypted with *Vigenère Cipher*. You can bruteforce it with an [on-line tool](https://www.dcode.fr/vigenere-cipher).

The encryption key is `AICGBIJC` and the decrypted text is the following.

```
Howdoyoukeepaprogrammerintheshowerallday?
GivehimabottleofshampoowhichsaysLatherrinserepeatDawgCTF{ClearEdge_crypto}
```

The flag is the following.

```
DawgCTF{ClearEdge_crypto}
```

## Tracking

* **Category:** web/networking
* **Points:** 100

### Challenge

> What's that pixel tracking?
> 
> https://clearedge.ctf.umbccd.io/
> 
> Author: ClearEdge

### Solution

The interesting part is the following.

```html
<img src=".." height="1px" width="1px" onclick="alert(String.fromCharCode(68,97,119,103,67,84,70,123,67,108,101,97,114,69,100,103,101,95,117,110,105,125))" >
```

Using browser console to run the JavaScript will give you the flag.

```
DawgCTF{ClearEdge_uni}
```