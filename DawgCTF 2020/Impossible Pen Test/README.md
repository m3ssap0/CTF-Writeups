# DawgCTF 2020 – Impossible Pen Test

These are multiple challenges connected together.

## Impossible Pen Test Part 1

* **Category:** forensics (OSINT)
* **Points:** 50

### Challenge

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the password of an affiliate's CEO somewhere on the internet and use it to log in to the corporate site? https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Solution

On the corporate website `https://theinternet.ctf.umbccd.io/burkedefensesolutions.html` you can discover the following message.

```
A message from our CEO
Special thanks to Todd Turtle from Combined Dumping & Co for babysitting our kids!

Special thanks to Mohamed Crane from Babysitting, LLC for helping us take out the trash!

Special thanks to Sonny Bridges from Oconnell Holdings for freeing up our finances!

Special thanks to Emery Rollins from Combined Finance, Engineering, Scooping, Polluting, and Dumping, Incorporated for helping make the world a better place!

- Truman Gritzwald, CEO
```

On the personal profile of Emery Rollins `` you can discover a post taling about a data breach.

```
OMG just found out about the charriottinternational data breach repo!
```

It seems that several people listed in the message of the CEO used that hotel.

Searching for the data breach will return: `https://theinternet.ctf.umbccd.io/SecLists/charriottinternational.txt`.

E-mails of the people can be found in their professional pages.

```
Todd Turtle
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BToddTurtle%7D.html
oxmf1yyzeka@sticky.com

Mohamed Crane
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BMohamedCrane%7D.html
cranemohameduuddyq@wemail.cc
mohamedc@chubby.com

Sonny Bridges
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BSonnyBridges%7D.html
bseok@parcel.com

Emery Rollins
https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BEmeryRollins%7D.html
rollinsemery@wemail.com
emeryrdzbiu@shy.com
```

Credentials for the Sonny Bridges e-mail can be found.

```
bseok@parcel.com        fr33f!n@nc3sf0r@ll!
```

Trying to login into corporate website will give you the flag.

```
DawgCTF{th3_w3@k3s7_1!nk}
```

## Impossible Pen Test Part 2

* **Category:** forensics (OSINT)
* **Points:** 50

### Challenge

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find a disgruntled former employee somewhere on the internet (their URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Solution

On the corporate website `https://theinternet.ctf.umbccd.io/burkedefensesolutions.html` you can discover the name of the CEO: `Truman Gritzwald`.

On its FaceSpace `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BTrumanGritzwald%7D.html` you can discover that he fired the CFO, so he could be the disgruntled former employee.

```
Nov 27, 2019
About to fire my CFO!
```

You can also discover the name of the CTO, Isabela Baker, and the name of Madalynn Burke.

Madalynn Burke is no more the CISO, according to her professional profile at `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BMadalynnBurke%7D.html`.

```
01/2020 - Present
Cybersanitation Engineer - Barber Pollute and Babysitting, Limited


09/2019 - 01/2020
CISO - Burke Defense Solutions & Management
```

But on her FaceSpace `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BMadalynnBurke%7D.html` you can discover another person: Royce Joyce, the CTO.

```
Sep 27, 2019
[Pictured: a hacker and some guy and my parents]
Great dinner with CTO Royce Joyce!
```

Analyzing the personal profile of Royce Joyce `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BRoyceJoyce%7D.html` you can discover other people named in a post.

```
Meet the team! Carlee Booker, Lilly Lin, Damian Nevado, Tristen Winters, Orlando Sanford, Hope Rocha, and Truman Gritzwald.
```

One of them, Tristen Winters, is the current Chief Information Security Officer and on his personal profile `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BTristenWinters%7D.html` warns about a person called Rudy Grizwald.

```
Nov 28, 2019
[Pictured: hackers]
Everyone should ignore Rudy Grizwald's messages
```

Analyzing the professional profile of Rudy Grizwald, `https://theinternet.ctf.umbccd.io/SyncedIn/DawgCTF%7BRudyGrizwald%7D.html`, you can discover he was the CFO.

```
11/2019 - Present
Data Breacher - Combined Teach, Inc.

1/2019 - 11/2019
Chief Financial Officer - Burke Defense Solutions & Management
```

And on the personal profile `https://theinternet.ctf.umbccd.io/FaceSpace/DawgCTF%7BRudyGrizwald%7D.html` you can discover he is mad at the CEO.

```
Nov 28, 2019
Truman Gritzwald is a bad CEO.
```

The flag is the following.

```
DawgCTF{RudyGrizwald}
```

## Impossible Pen Test Part 3

* **Category:** forensics (OSINT)
* **Points:** 100

### Challenge

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the mother of the help desk employee's name with their maiden name somewhere on the internet (the mother's URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Solution

One of the people discovered before, Orlando Sanford, is the Help Desk Worker, accordig to his professional profile at `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BOrlandoSanford%7D.html`.

Analyzing his personal profile at `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BOrlandoSanford%7D.html` you can discover a post referred to his mother.

```
Jun 01, 2018
[Pictured: Alexus Cunningham]
My mom defenestrates a cat!
```

Checking on her personal profile `https://theinternet.ctf.umbccd.io/FaceSpace/DawgCTF%7BAlexusCunningham%7D.html` you can confirm she is his mother.

```
Alexus Cunningham

In a relationship with: Marely Bruce
Child: Orlando Sanford
```

So the flag is the following.

```
DawgCTF{AlexusCunningham}
```

## Impossible Pen Test Part 4

* **Category:** forensics (OSINT)
* **Points:** 100

### Challenge

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the syncedin page of the linux admin somewhere on the internet (their URL will be the flag)?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Solution

Hope Rocha, discovered before, was a Linux admin, according to his professional profile on SyncedIn `https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BHopeRocha%7D.html`, but he is not the current one.

```
12/2018 - 08/2019
Linux Admin - Burke Defense Solutions & Management
```

According to his personal profile `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BHopeRocha%7D.html` the new Linux admin is Guillermo McCoy.

```
Aug 18, 2018
[Pictured: Guillermo McCoy]
Meet your new Linux Admin for Burke Defense Solutions & Management!
```

Checking his professional profile at `https://theinternet.ctf.umbccd.io/SyncedIn/DawgCTF%7BGuillermoMcCoy%7D.html` will reveal that it's correct.

```
Guillermo McCoy

mccoyggwe3@yam.com
2jabjj5mm3m@stupid.io
gm5f@judicious.com
guillermomm3rcr@homeschool.com
mguillermo@wemail.cc

08/2019 - Present
Linux Admin - Burke Defense Solutions & Management
```

So the flag is the following.

```
DawgCTF{GuillermoMcCoy}
```

## Impossible Pen Test Part 5

* **Category:** forensics (OSINT)
* **Points:** 100

### Challenge

> Welcome! We're trying to hack into Burke Defense Solutions & Management, and we need your help. Can you help us find the CTO's password somewhere on the internet and use it to log in to the corporate site?
> 
> https://theinternet.ctf.umbccd.io/
> 
> (no web scraping is required to complete this challenge)
> 
> author: pleoxconfusa

### Solution

Royce Joyce is the CTO and he has two e-mails (`https://theinternet.ctf.umbccd.io/SyncedIn/DogeCTF%7BRoyceJoyce%7D.html`).

```
roycejoyce@wemail.net
jr7lp@homeschool.com
```

Analyzing his personal profile `https://theinternet.ctf.umbccd.io/FaceSpace/DogeCTF%7BRoyceJoyce%7D.html` you can discover a data breach.

```
Sep 07, 2019
Apparently skayou had a data breach? LOL
```

Searching for the data breach will return: `https://theinternet.ctf.umbccd.io/SecLists/skayou.txt`.

And one of its e-mails can be found with a password.

```
roycejoyce@wemail.net	c0r^3cth0rs3b@tt3ryst@p\3
```

Trying to login into corporate website will give you the flag.

```
DawgCTF{xkcd_p@ssw0rds_rul3}
```