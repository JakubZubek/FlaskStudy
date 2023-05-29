from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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