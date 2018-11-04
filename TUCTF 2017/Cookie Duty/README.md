# TUCTF 2017 – Cookie Duty

* **Category:** web
* **Points:** 50

## Challenge

> You have been summoned for Jury Duty. Try out the new web form with a state-of-the-art authentication system.
>
> [http://cookieduty.tuctf.com](http://cookieduty.tuctf.com)

## Solution

After submitting the form you can see a cookie:

```
not_admin : 1
```

It's sufficient to change that cookie to the value 0 and to refresh the page in order to retrieve the flag:

```
TUCTF{D0nt_Sk1p_C00k13_Duty}
```