# ångstromCTF 2020 – Woooosh

* **Category:** web
* **Points:** 130

## Challenge

> Clam's tired of people hacking his sites so he spammed obfuscation on his new game. I have a feeling that behind that wall of obfuscated javascript there's still a vulnerable site though. Can you get enough points to get the flag? I also found the backend source.
> 
> Author: aplet123
> 
> Hint: The frontend is obfuscated but maybe something else isn't?

## Solution

The website is a game where you have to click on the circle and don't click on the squares, both located on random positions each round. You have to click more than 20 times in 10 seconds.

```html
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <link href="https://fonts.googleapis.com/css?family=Inter&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    
        <title>Woooosh</title>

        <script src="/socket.io/socket.io.js"></script>
    </head>
    <body>
        <h1>The Greatest Game of All Time</h1>
<p>If I aggressively obfuscate the frontend then my code is secure, right?</p>
<p id="pScore">To play, just click on the circle and don't click on the square.</p>
<button id="bStart">Start game</button>
<canvas id="cGame" width="500" height="300"></canvas>
<script src="main.js"></script>
    </body>
</html>
```

The [frontend source](main.js) is heavily obfuscated, but the challenge gives you the [backend source](index.js).

```javascript
const express = require("express");
const exphbs = require("express-handlebars");
const socket = require("socket.io");
const path = require("path");
const http = require("http");
const morgan = require("morgan");

const app = express();
const serv = http.createServer(app);
const io = socket.listen(serv);
const port = process.env.PORT || 60600;

function rand(bound) {
    return Math.floor(Math.random() * bound);
}

function genId() {
    const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    return new Array(64).fill(0).map(v => chars[rand(chars.length)]).join``;
}

function genShapes() {
    return new Array(20).fill(0).map(v => ({ x: rand(500), y: rand(300) }));
}

function dist(a, b, c, d) {
    return Math.sqrt(Math.pow(c - a, 2), Math.pow(d - b, 2));
}

app.use(morgan("combined"));

app.use(express.static(path.join(__dirname, "public")));

const hbs = exphbs.create({
    extname: ".hbs",
    helpers: {}
});

app.engine("hbs", hbs.engine);
app.set("view engine", "hbs");
app.set("views", path.join(__dirname, "views"));

io.on("connection", client => {
    let game;
    setTimeout(function() {
        try {
            client.disconnect();
        } catch (err) {
            console.log("err", err);
        }
    }, 1 * 60 * 1000);
    function endGame() {
        try {
            if (game) {
                if (game.score > 20) {
                    client.emit(
                        "disp",
                        `Good job! You're so good at this! The flag is ${process.env.FLAG}!`
                    );
                } else {
                    client.emit(
                        "disp",
                        "Wow you're terrible at this! No flag for you!"
                    );
                }
                game = null;
            }
        } catch (err) {
            console.log("err", err);
        }
    }
    client.on("start", function() {
        try {
            if (game) {
                client.emit("disp", "Game already started.");
            } else {
                game = {
                    shapes: genShapes(),
                    score: 0
                };
                game.int = setTimeout(endGame, 10000);
                client.emit("shapes", game.shapes);
                client.emit("score", 0);
            }
        } catch (err) {
            console.log("err", err);
        }
    });
    client.on("click", function(x, y) {
        try {
            if (!game) {
                return;
            }
            if (typeof x != "number" || typeof y != "number") {
                return;
            }
            if (dist(game.shapes[0].x, game.shapes[1].y, x, y) < 10) {
                game.score++;
            }
            game.shapes = genShapes();
            client.emit("shapes", game.shapes);
            client.emit("score", game.score);
        } catch (err) {
            console.log("err", err);
        }
    });
    client.on("disconnect", function() {
        try {
            if (game) {
                clearTimeout(game.int);
            }
            game = null;
        } catch (err) {
            console.log("err", err);
        }
    });
});

app.get("/", function(req, res) {
    res.render("home");
});

serv.listen(port, function() {
    console.log(`Server listening on port ${port}!`);
});
```

From this source code you can discover that positions are sent to the client into a JSON array and that the winning position is the first one sent.

Analyzing the HTTP traffic you can discover the format of each request/response packet and you can use this information to develop [your own client](solver-woooosh.py) able to win each round of the game.

```python
#!/usr/bin/python

import requests
import time
import math

verbose = True

target_site = "https://wooooosh.2020.chall.actf.co/"
target_endpoint_without_sid = target_site + "socket.io/?EIO=3&transport=polling&t={}"
target_endpoint = target_endpoint_without_sid + "&sid={}"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "text/plain;charset=UTF-8",
   "Accept-Encoding": "gzip, deflate, br",
   "Origin": "https://wooooosh.2020.chall.actf.co",
   "Referer": "https://wooooosh.2020.chall.actf.co/",
}

def log_message(message):
    if verbose:
        print(message)


def log_data(answer):
    if verbose:
        print("-----------------------------------")
        print(answer)
        print("-----------------------------------")


def get_sid_from_cookies(cookies):
    sid = None
    #log_message("[*] Cookies:")
    for cookie in cookies:
        #log_message("[*]   - {}={}".format(cookie.name, cookie.value))
        if cookie.name == "io":
            sid = cookie.value
            #log_message("[*] Found sid: {}.".format(sid))
    return sid


def generate_t_param():
    timestamp = int(round(time.time() * 1000))
    return yeast_encode(timestamp)


# https://github.com/unshiftio/yeast/blob/28d15f72fc5a4273592bc209056c328a54e2b522/index.jsL17
def yeast_encode(num):
    alphabet = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_")
    length = len(alphabet)
    encoded = ""
    
    while True:
        encoded = alphabet[num % length] + encoded
        num = math.floor(num / length)
        if num <= 0:
            break
    
    return encoded


def generate_payload(payload):
    return "{}:{}".format(str(len(payload)), payload)


def generate_start_payload():
    start_payload = generate_payload("42[\"start\"]")
    #log_data(start_payload)
    return start_payload


def generate_answer_payload(x, y):
    answer_payload = generate_payload("42[\"click\",{},{}]".format(x, y))
    #log_data(answer_payload)
    return answer_payload


t = generate_t_param()
url = target_endpoint_without_sid.format(t)
#log_message("[*] Getting sid. {}".format(url))
r = requests.get(url, headers=headers)
cookies = r.cookies
#log_data(r.text)
sid = get_sid_from_cookies(cookies)

t = generate_t_param()
url = target_endpoint.format(t, sid)
#log_message("[*] Starting the game. {}".format(url))
r = requests.post(url, headers=headers, cookies=cookies, data=generate_start_payload())
cookies = r.cookies
#log_data(r.text)

#log_message("[*] Playing the game.")
score = ""
start_time = int(round(time.time() * 1000))
bad_gateway_retries = 0
while True:

    while True:
        t = generate_t_param()
        url = target_endpoint.format(t, sid)
        #log_message("[*] Polling. {}".format(url))
        r = requests.get(url, headers=headers, cookies=cookies)
        cookies = r.cookies
        content = r.text
        #log_data(content)
    
        if r.status_code == 502:
            bad_gateway_retries += 1
            t = generate_t_param()
            url = target_endpoint_without_sid.format(t)
            #log_message("[*] Getting sid. {}".format(url))
            r = requests.get(url, headers=headers)
            cookies = r.cookies
            #log_data(r.text)
            sid = get_sid_from_cookies(cookies)
        else:
            break
    
    if "actf{" in content:
        print("                                         ")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] vvvvvvvvvvvv FLAG FOUND! vvvvvvvvvvvv")
        print("                                         ")
        print(content)
        print("                                         ")
        print("[*] ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] =====================================")
        print("                                         ")
        break
    elif "terrible" in content or "disconnected" in content:
        end_time = int(round(time.time() * 1000))
        total_time = (end_time - start_time) / 1000
        print("[*] FAILED! Score: {} ({} secs, {} 502 retries)".format(score, str(total_time), str(bad_gateway_retries)))
        break
    elif "shapes" in content:
        #log_message("[*][shapes] Response intercepted.")
        coordinates = content[21:34].replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("\"", "").replace("x", "").replace("y", "").replace(":", "")
        best_x = coordinates.split(",")[0]
        best_y = coordinates.split(",")[1]
        #log_message("[*][shapes] The best position is at {}, {}.".format(best_x, best_y))
        if "score" in content:
            score = content[-5:-1].replace("]", "").replace(",", "").replace("\"", "").replace("e", "")
            #log_message("[*][shapes] Score: {}.".format(score))
        t = generate_t_param()
        url = target_endpoint.format(t, sid)
        #log_message("[*] Send answer. {}".format(url))
        r = requests.post(url, headers=headers, cookies=cookies, data=generate_answer_payload(best_x, best_y))
        cookies = r.cookies
        content = r.text
        #log_data(content)
    elif "score" in content:
        #log_message("[*][score] Response intercepted.")
        score = content[-5:-1].replace("]", "").replace(",", "").replace("\"", "").replace("e", "")
        #log_message("[*][score] Score: {}.".format(score))
```

The flag is the following.

```
actf{w0000sh_1s_th3_s0und_0f_th3_r3qu3st_fly1ng_p4st_th3_fr0nt3nd}
```