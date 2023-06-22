from flask import Flask, render_template, url_for, request, g, redirect, flash, session
import sqlite3
import random
import string
import hashlib
import binascii

app = Flask(__name__)
app.config["SECRET_KEY"]="aiwusdh6738r52$bkvsd"
app_info = { "db_file" : r"C:\Users\Anzel\Desktop\Projekty\FlaskStudy\data\users.db" }

def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
        return g.sqlite_db 
    
@app.teardown_appcontext 
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close() 


class UserPass:
    def __init__(self, user="", password=""):
        self.user = user
        self.password = password

    '''    def hash_password(self):
        random_os = "b'\xf41\xa2u\x1a[\xb0Hv\xe6Y ql\xe7\x02)\x04\x8bLd&\x93`\xcd\xb6\xf9x\xca\x8d(;\xd1\\<\xe4E9`I\xff4\x91\xf1\x99hKO\xfa\x8dR\xac\xeb\xaf}\xbd\xc6\x18\x9d`'"
        salt = hashlib.sha256(random_os.encode('utf-8')).hexdigest().encode('ascii')
        self.password = self.password.encode("utf-8")
        passwordhash = hashlib.pbkdf2_hmac('sha512', self.password, salt, 100000)
        passwordhash = binascii.hexlify(passwordhash)
        return (salt + passwordhash).decode("ascii")'''
    
    def verify_password(self, stored_password, provided_password):
        '''        salt = stored_password[:64]
        stored_password = stored_password[64:]
        passwordhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode("utf-8"), salt.encode("ascii"), 100000)
        passwordhash = binascii.hexlify(passwordhash).decode("ascii")'''
        return provided_password == stored_password
    
    def create_random_password(self):
        random_user = "".join(random.choice(string.ascii_lowercase)for i in range(3))
        print(random_user)
        self.user = random_user

        password_characters = string.ascii_letters
        random_password = "".join(random.choice(password_characters)for i in range(3))
        print(random_password)
        self.password = random_password
    
    def login_user(self):

        db = get_db()
        sql_statement = "select id, name, email, password, is_author, is_admin from users where name=?"
        cur = db.execute(sql_statement, [self.user])
        user_record = cur.fetchone()

        if user_record != None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

@app.route("/init_app")
def init_app():

 # check if there are users defined (at least one active admin required)
 db = get_db()
 sql_statement = 'select count(*) as cnt from users where is_author and is_admin;'
 cur = db.execute(sql_statement)
 active_admins = cur.fetchone()

 if active_admins!=None and active_admins['cnt']>0:
    #flash('Application is already set-up. Nothing to do')
    return redirect(url_for('index'))

 user_pass = UserPass()
 user_pass.create_random_password()
 sql_statement = '''insert into users(name, email, password, is_author, is_admin)
 values(?,?,?,True, True);'''
 db.execute(sql_statement, [user_pass.user, 'noone@nowhere.no', user_pass.password])
 db.commit()
 print(user_pass.user, user_pass.password) #fvd b'wSg
 return redirect(url_for('index')) 

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
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", active_menu="login")
    else:
        user_name = "" if "user_name" not in request.form else request.form["user_name"]
        user_password = "" if "user_password" not in request.form else request.form["user_password"]

        login = UserPass(user_name, user_password)
        login_record = login.login_user()

        if login_record != None:
            session["user"] = user_name
            return redirect(url_for("index"))
        else:
            return render_template("login.html")

if __name__ == "main":
    app.run(debug=True)