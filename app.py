from flask import Flask, render_template, url_for, request
import random
import string
import hashlib
import binascii

app = Flask(__name__)


class UserPass:
    def __init__(self, user="", password=""):
        self.user = user
        self.password = password
    def hash_password(self):
        random_os = "b'\xf41\xa2u\x1a[\xb0Hv\xe6Y ql\xe7\x02)\x04\x8bLd&\x93`\xcd\xb6\xf9x\xca\x8d(;\xd1\\<\xe4E9`I\xff4\x91\xf1\x99hKO\xfa\x8dR\xac\xeb\xaf}\xbd\xc6\x18\x9d`'"
        salt = hashlib.sha256(random_os).hexdigest().encode('ascii')
        passwordhash = hashlib.pbkdf2_hmac('sha512', self.password.encode("utf-8"), salt, 100000)
        passwordhash = binascii.hexlify(passwordhash)
        return (salt + passwordhash).decode("ascii")
    def verify_password(self):
        pass




@app.route("/")
def index():
    return (render_template("index.html", active_menu="home"))

@app.route("/about")
def about():
    return (render_template("about.html", active_menu="about"))

@app.route("/activites")
def activites():
    return (render_template("activites.html", active_menu="activites"))

@app.route("/creators")
def creators():
    return (render_template("creators.html", active_menu="creators"))



if __name__ == "main":
    app.run(debug=True)