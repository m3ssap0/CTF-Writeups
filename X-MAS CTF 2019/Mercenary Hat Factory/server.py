#!/usr/bin/env python3
from flask import Flask, render_template, render_template_string, request, redirect, make_response
import jwt, html, hashlib, random
from config import *

port = 2000
app = Flask (__name__, static_url_path = "/static")

users = {}
authorizedAdmin = {}
adminPrivileges = [[None]*3]*500

adminPrivileges [0][0] = 0 # UID
adminPrivileges [0][1] = "Santa" #Uname
adminPrivileges [0][2] = SantaSecret

@app.route ('/', methods = ['GET'])
def index():
    token = request.cookies.get ("auth")

    if (token != None):
        userData = DecodeJWT (token)
        try:
            admin = False
            authorized = False

            if (userData ["type"] == "admin"):
                admin = True

            if (userData["user"] in authorizedAdmin):
                authorized = True

            resp = render_template ("index.html", loggedIn = True, user = userData["user"], admin = admin, authorized = authorized)
        except:
            resp = render_template ("index.html", loggedIn = False)
    else:
        resp = render_template ("index.html", loggedIn = False)

    return resp

@app.route ('/register', methods=['GET', 'POST'])
def register ():
    if (request.method == 'GET'):
        resp = render_template ("action.html", action="register")
    elif (request.method == 'POST'):
        user = request.form.get ('user')
        passwd = request.form.get ('pass')

        if (user not in users):
            users[user] = passwd
            token = jwt.encode ({'type': 'user', 'user':user}, JWTSecret, algorithm = 'HS256')
            resp = make_response (redirect ("/"))
            resp.set_cookie ('auth', token)
        else:
            resp = render_template ("error.html", error = "User already exists.")
    return resp

@app.route ('/login', methods=['GET', 'POST'])
def login ():
    if (request.method == 'GET'):
        resp = render_template ("action.html", action="login")
    elif (request.method == 'POST'):
        user = request.form.get ('user')
        passwd = request.form.get ('pass')

        if (user in users):
            if (users[user] == passwd):
                token = jwt.encode ({'type': 'user', 'user':user}, JWTSecret, algorithm = 'HS256')
                resp = make_response (redirect ("/"))
                resp.set_cookie ('auth', token)
            else:
                resp = render_template ("error.html", error = "Wrong password.")
        else:
            resp = render_template ("error.html", error = "No such user.")

    return resp

@app.route ('/logout', methods=['GET', 'POST'])
def logout ():
    resp = make_response (render_template ("index.html", loggedIn = False))
    resp.set_cookie ('auth', '')
    return resp

@app.route ('/authorize', methods=['POST'])
def authorize ():
    token = request.cookies.get ("auth")

    if (token != None):
        try:
            userData = DecodeJWT (token)

            if (userData["type"] != "admin"):
                return render_template ("error.html", error = "Unauthorized.")

            uid = 1
            hsh = hashlib.md5 (userData ["user"].encode ()).hexdigest ()

            for c in hsh:
                if (c in "0123456789"):
                    uid += int (c)

            step = int (request.args.get ("step"))
            if (step == 1):
                adminPrivileges [uid][0] = uid
                adminPrivileges [uid][1] = userData ["user"]
                adminPrivileges [uid][2] = request.form.get ('privilegeCode')
                resp = make_response (redirect ("/"))
            elif (step == 2):
                userpss = adminPrivileges [uid][2]
                # Is the user actually santa?
                uid = adminPrivileges [0][0]
                usr = adminPrivileges [0][1]
                pss = adminPrivileges [0][2]

                if (request.form.get ('accessCode') == str (uid) + usr + pss + userpss):
                    authorizedAdmin [userData ["user"]] = True
                    #os.system ("curl https://lapland.htsp.ro/adminauth") # Announce new admin authorization

                    resp = make_response (redirect ("/"))
                else:
                    resp = render_template ("error.html", error = "Access Code is incorrect.")
            else:
                resp = render_template ("error.html", error = "Unauthorized.")
        except:
            resp = render_template ("error.html", error = "Unknown Error.")
    else:
        resp = render_template ("error.html", error = "Unauthorized.")

    return resp

@app.route ('/makehat', methods=['GET'])
def makehat ():
    hatName = request.args.get ("hatName")
    token = request.cookies.get ("auth")
    blacklist = ["config", "self", "request", "[", "]", '"', "_", "+", " ", "join", "%", "%25"]

    if (hatName == None):
    	return render_template ("error.html", error = "Your hat has no name!")

    for c in blacklist:
        if (c in hatName):
            return render_template ("error.html", error = "That's a hella weird Hat Name, maggot.")

    if (len (hatName.split (",")) > 2):
        return render_template ("error.html", error = "How many commas do you even want to have?")

    page = render_template ("hat.html", hat = random.randint (0, 9), hatName = hatName)

    if (token != None):
        userData = DecodeJWT (token)
        try:
            authorized = False
            if ((userData["user"] in authorizedAdmin) and (users[userData["user"]] == userData["pass"])):
                authorized = True # and what
                resp = render_template_string (page)
            else:
                resp = render_template ("error.html", error = "Unauthorized.")
        except:
            resp = render_template ("error.html", error = "Error in viewing hat.")
    else:
        resp = render_template ("error.html", error = "Unauthorized.")
    
    return resp

if __name__ == '__main__':
    app.run (host = '0.0.0.0', port = port)