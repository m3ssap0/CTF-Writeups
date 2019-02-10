# Evlz CTF 2019 – Portability

* **Category:** Misc
* **Points:** 25

## Challenge

> My beautiful API is finally ready! Uses Flask, Virtual Environments, and loads the config from Environment Variables! 
>
> [Download](portability.zip)

## Solution

The challenge provides an archive containing the application source code, repository and libraries.

Analyzing the `handout/application.py` file, you can discover that the application reads from an environment variable.

```python
FLAG = os.getenv("FLAG", "evlz{}ctf")


@app.route('/beauty', methods=["GET"])
def beauty():
    return jsonify({
        'flag': FLAG
    })
```

Into the `handout/env/bin/activate` file there is a suspect `export` command.

```bash
export $(echo RkxBRwo= | base64 -d)=ZXZsenthbHdheXNfaWdub3JlX3RoZV91bm5lY2Nlc3Nhcnl9Y3RmCg=
```

Decoding the base64 string `ZXZsenthbHdheXNfaWdub3JlX3RoZV91bm5lY2Nlc3Nhcnl9Y3RmCg=` will reveal the flag.

```
evlz{always_ignore_the_unneccessary}ctf
```