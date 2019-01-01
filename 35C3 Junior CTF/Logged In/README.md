# 35C3 Junior CTF – Logged In

* **Category:** Web
* **Points:** 47 (variable)

## Challenge

> Phew, we totally did not set up our mail server yet. This is bad news since nobody can get into their accounts at the moment... It'll be in our next sprint. Until then, since you cannot login: enjoy our totally finished software without account.
>
> http://35.207.189.79/
>
> ===============================================
>
> Good coders should learn one new language every year.
>
> InfoSec folks are even used to learn one new language for every new problem they face (YMMV).
>
> If you have not picked up a new challenge in 2018, you're in for a treat.
>
> We took the new and upcoming Wee programming language from paperbots.io. Big shout-out to Mario Zechner (@badlogicgames) at this point.
>
> Some cool Projects can be created in Wee, like: this, this and that.
>
> Since we already know Java, though, we ported the server (Server.java and Paperbots.java) to Python (WIP) and constantly add awesome functionality. Get the new open-sourced server at /pyserver/server.py.
>
> Anything unrelated to the new server is left unchanged from commit dd059961cbc2b551f81afce6a6177fcf61133292 at badlogics paperbot github (mirrored up to this commit here).
>
> We even added new features to this better server, like server-side Wee evaluation!
>
> To make server-side Wee the language of the future, we already implemented awesome runtime functions. To make sure our VM is 100% safe and secure, there are also assertion functions in server-side Wee that you don't have to be concerned about.

## Solution

The web site does not send double opt-in e-mail. A user can be registered, but the e-mail with the "magic code" needed to login will not be received.

Analyzing the response of the authentication API (i.e. `http://35.207.189.79/api/login`) a code can be found in the payload returned by the server. That code is the magic one that must be inserted in the window to complete the login.

After the login, a cookie will be set with the flag.

```
logged_in : 35C3_LOG_ME_IN_LIKE_ONE_OF_YOUR_FRENCH_GIRLS
```