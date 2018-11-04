# Access Denied 1.2 2018 – Ghus Ke Dikhao

* **Category:** web
* **Points:** 200

## Challenge

> Rahul is a cheater !! Rahul is a cheater !!....
>
> So, Anjali made sure Rahul doesn't get access to her website as he is not admin.
>
> But Rahul is a Sai Baba devotee and he believes in "Sabka Malik = 1"
>
> Challenge running at : [http://18.217.96.77:8081/](http://18.217.96.77:8081/)

## Solution

The website home page contains a login form.

Analyzing browser cookies, you can find the following one:

```
admin_id : 0
```

Changing it to `1` and refreshing the page will give you the flag.

```
accessdenied{4ye_4ye_4dm1n_xadv184v}
```