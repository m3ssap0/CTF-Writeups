# Access Denied 1.2 2018 – JS and JQuery

* **Category:** web
* **Points:** 175

## Challenge

> JS was very happy with his abilities. But JQuery gave him superpower.
>
> And we all know - **With great power comes great responsibility.**
>
> Challenge running at : [http://18.217.96.77:8080/](http://18.217.96.77:8080/)

## Solution

Analyzing the browser console, you can find an error:

```
jquery-3.3.1.min.js:2 Uncaught SyntaxError: Unexpected token {
```

Going to that portion of the JavaScript file will reveal the flag:

```
accessdenied{1t_w4s_h1dd3n_h3r3_594a9sd}
```