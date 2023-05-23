from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return (render_template("index.html"))

@app.route("/about")
def about():
    return (render_template("about.html"))

@app.route("/activites")
def activites():
    return (render_template("activites.html"))

@app.route("/creators")
def creators():
    return (render_template("creators.html"))



if __name__ == "main":
    app.run(debug=True)