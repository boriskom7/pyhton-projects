from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from datetime import date, datetime, time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrettodolistpassword1'
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        timer = request.form["time-options"]
        mode = request.form["mode"]
        return redirect(url_for("type_now", timer=timer, mode=mode))
    return render_template("home.html")


@app.route('/type/<string:mode>/<int:timer>', methods=["GET", "POST"])
def type_now(timer,mode):
    return render_template("type.html", timer=timer, mode=mode)


if __name__ == "__main__":
    app.run(debug=True)
