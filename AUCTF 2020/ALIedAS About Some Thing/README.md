# AUCTF 2020 – ALIedAS About Some Thing

* **Category:** OSINT
* **Points:** 903

## Challenge

> See what you can find.
> 
> AUCTFShh
> 
> Author: c


## Solution

You can use [*UserFinder*](https://github.com/tr4cefl0w/userfinder) to search the given string, in order to discover if it is used as a username.

```
user@machine:~/tools/userfinder$ python3 userfinder.py AUCTFShh

 _   _               _____ _           _
| | | |___  ___ _ __|  ___(_)_ __   __| | ___ _ __
| | | / __|/ _ \ '__| |_  | | '_ \ / _` |/ _ \ '__|
| |_| \__ \  __/ |  |  _| | | | | | (_| |  __/ |
 \___/|___/\___|_|  |_|   |_|_| |_|\__,_|\___|_|

by tr4cefl0w

[*] Searching...
[+] Profile found: https://twitter.com/AUCTFShh
[+] Profile found: https://www.reddit.com/user/AUCTFShh
[+] Profile found: https://steamcommunity.com/id/AUCTFShh
[+] Profile found: https://imgur.com/user/AUCTFShh
[+] Profile found: https://open.spotify.com/user/AUCTFShh
[+] Profile found: https://www.skyscanner.fr/?previousCultureSource=GEO_LOCATION&redirectedFrom=www.skyscanner.net
```

On Steam (`https://steamcommunity.com/id/AUCTFShh`) you can discover that the user has an alias: `youllneverfindmese`. So you can try to search for it.

```
user@machine:~/tools/userfinder$ python3 userfinder.py youllneverfindmese


| | | |___  ___ _ __|  ___(_)_ __   __| | ___ _ __
| | | / __|/ _ \ '__| |_  | | '_ \ / _` |/ _ \ '__|
| |_| \__ \  __/ |  |  _| | | | | | (_| |  __/ |
 \___/|___/\___|_|  |_|   |_|_| |_|\__,_|\___|_|

by tr4cefl0w

[*] Searching...
[+] Profile found: https://twitter.com/youllneverfindmese
[+] Profile found: https://imgur.com/user/youllneverfindmese
[+] Profile found: https://open.spotify.com/user/youllneverfindmese
[+] Profile found: https://pastebin.com/u/youllneverfindmese
[+] Profile found: https://www.skyscanner.fr/?previousCultureSource=GEO_LOCATION&redirectedFrom=www.skyscanner.net
```

The PasteBin account (`https://pastebin.com/u/youllneverfindmese`) contains an interesting untitled file: `https://pastebin.com/qMRYqzYB`.

The content of the file is the following.

```
https://devs-r-us.xyz/jashbsdfh1j2345566bqiuwhwebjhbsd/flag.txt
```

Connecting to the webpage will give you the flag.

```
auctf{4li4s3s_w0nT_5t0p_m3_6722df34df}
```