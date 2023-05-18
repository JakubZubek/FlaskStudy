from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return (render_template("index.html"))

@app.route("/chess", methods=["GET", "POST"])
def chess():
    if request.method == "GET":
        return render_template("chess.html")
    else:
        if "note" in request.form:
            note = request.form['note']
        if "note" in request.form:
            comment = request.form['comment']
        if 'decision' in request.form:
            decision = "to recommand everyone!"
        else:
            decision = "to not recommand for anyone!"
        return render_template("chess_return.html", note=note, comment=comment, decision=decision)

if __name__ == "main":
    app.run(debug=True)