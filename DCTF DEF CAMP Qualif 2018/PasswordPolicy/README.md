# DCTF DEF CAMP Qualif 2018 – PasswordPolicy

* **Category:** web
* **Points:** 1

## Challenge

> Can you guess this extreme password?
>
> Target: [https://password-policy.dctfq18.def.camp/](https://password-policy.dctfq18.def.camp/)

## Solution

The target website contains a login form with a JavaScript check used to prevent the submission of long passwords.

```javascript
    $('form').submit(function(e) {
      if($('input[name="pass"]').val().length < 1337) {
          alert('Minimum length for password is 1337 characters.');
          e.preventDefault();
          return false;
      }
  });
```

JavaScript can be easily disabled from the browser (or a proxy tool can be used to intercept and repeat the request) in order to bypass this check.

Using a common password, i.e. `password`, will reveal the flag:

```
DCTF{db95ace20ae3972f87d758a3724142ae93735c442a8482f9717fe4a9bb94d337}
```