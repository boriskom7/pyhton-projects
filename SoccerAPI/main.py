from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

from data import Data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrettodolistpassword1'
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/standings/<string:league_name>', methods=["GET", "POST"])
def show_league(league_name):
    data = Data(league_name)
    league_data = data.league
    team_data = data.teams[0]
    return render_template("standings.html", league_data=league_data, team_data=team_data)

if __name__ == "__main__":
    app.run(debug=True)
