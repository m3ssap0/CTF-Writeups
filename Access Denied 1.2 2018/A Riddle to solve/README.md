# Access Denied 1.2 2018 – A Riddle to solve

* **Category:** crypto
* **Points:** 50

## Challenge

> "A coward dies a thousand times before his death, but the valiant taste of death but once. It seems to me most strange that men should fear, seeing that death, a necessary end, will come when it will come."
> Are you valiant enough to find the flag?
> Download file from : https://accessd.sfo2.digitaloceanspaces.com/crypto50.txt
> TAKE CARE OF CASE SENSITIVITY

## Solution

The quote is from William Shakespeare's *Julius Caesar*, so the [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher) must be involved.

The content of the downloaded file is the following:

```
tvvxllwxgbxw{pX_TkX_UX_VHeExZx_tlwpYP}
```

Considering that the first letter must be an `a`, due to flag syntax, the rotation should be of 7 places (i.e. ROT7).

An [on-line service](https://www.rot13.com/) can be used to obtain the flag:

```
accessdenied{wE_ArE_BE_COlLeGe_asdwFW}
```