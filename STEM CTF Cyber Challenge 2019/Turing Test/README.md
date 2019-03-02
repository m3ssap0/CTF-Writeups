# STEM CTF Cyber Challenge 2019 – Turing Test

* **Category:** Web
* **Points:** 50

## Challenge

> Break into his account!
> 
> http://138.247.13.111

## Solution

The shown web page seems to perform a password reset functionality via security questions. It seems to be related to the account recovery of *Alan Turing*.

If you submit data, the web page will highlight in red wrong fields.

Some recon activities on the Internet about Alan Turing must be done in order to answer security questions.

After few attepts you will discover all the answers:
* Text field - *Mother's Maiden Name* - Stoney
* Text field - *First School Attended* - St. Michael's
* Text field - *Favorite Primary School Subject* - Science
* Text field - *Favorite Olympic Event* - Marathon
* Text field - *2 + 2 - 3 = ?* - 1
* Checkbox - *Is it a leap year?* - checked
* Checkbox - *I agree Security Questions are Bad.* - checked

The flag is the following.

```
MCA{sms_2fa_is_bad_also}
```