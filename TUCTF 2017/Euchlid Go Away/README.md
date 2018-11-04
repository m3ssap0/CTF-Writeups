# TUCTF 2017 – Euchlid Go Away

* **Category:** vm
* **Points:** 150

## Challenge

> Come play the hottest new text based dungeon crawler! Yours for a limited time only!

```
nc euchlidgoaway.tuctf.com 6662
```

## Solution

This is a vulnerable text-based dungeon crawler game.

Steps to solve it:
* You have to login with the name of an administrator (i.e. `whoisjohngalt`), discovered during a previous play.
* The next step is to move through the dungeon, in order to fight enemies and reach level 2.
* Now an admin can be contacted via message with subject `bugged leveling`.
* At this point you have to set the value of the new level to 256.
* Your user will have administrative role (the important thing is to have the name of an admin, otherwise an error will be spawned and the game will end).
* Using the new admin `(T)eleport` functionality, you can teleport to the `Developer Room (28)` and discover that there is something strange with received messages, because there is a shell-like error.
* Using the new admin `(T)eleport` functionality, you can teleport to `Admin Room (27)` in order to leave a message to the developers: `ls .`.
* Visiting the `Developer Room`, the `ls` command will be executed, showing a `flag.txt` file.
* The next message to send will be: `cat flag.txt`.
* Visiting the `Developer Room` and reading the message will reveal the flag.

The flag is:

```
TUCTF{you_hax0rs_get_outta_my_game}
```