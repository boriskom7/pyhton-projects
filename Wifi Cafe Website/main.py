from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, URL
#from flask_ckeditor import CKEditor, CKEditorField



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

#with app.app_context():
#    db.create_all()

#WTForm
class CafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Cafe map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe location", validators=[DataRequired()])
    has_sockets = BooleanField("Sockets?", validators=[])
    has_toilet = BooleanField("Toilet?", validators=[])
    has_wifi = BooleanField("WiFi?", validators=[])
    can_take_calls = BooleanField("Calls?", validators=[])
    seats = IntegerField("Number of seats", validators=[DataRequired()])
    coffee_price = FloatField("Coffee price", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/new', methods=["GET", "POST"])
def new():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = form.has_sockets.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            can_take_calls = form.can_take_calls.data,
            seats = form.seats.data,
            coffee_price = form.coffee_price.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new.html", form=form)

@app.route('/delete/<int:cafe_id>')
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))





@app.route('/edit/<int:cafe_id>', methods=["GET", "POST"])
def edit(cafe_id):
    cafe_to_edit = Cafe.query.get(cafe_id)

    edit_form = CafeForm(
        name = cafe_to_edit.name,
        map_url = cafe_to_edit.map_url,
        img_url = cafe_to_edit.img_url,
        location = cafe_to_edit.location,
        has_sockets = cafe_to_edit.has_sockets,
        has_toilet = cafe_to_edit.has_toilet,
        has_wifi = cafe_to_edit.has_wifi,
        can_take_calls = cafe_to_edit.can_take_calls,
        seats = cafe_to_edit.seats,
        coffee_price = cafe_to_edit.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe_to_edit.name = edit_form.name.data
        cafe_to_edit.map_url = edit_form.map_url.data
        cafe_to_edit.img_url = edit_form.img_url.data
        cafe_to_edit.location = edit_form.location.data
        cafe_to_edit.has_sockets = edit_form.has_sockets.data
        cafe_to_edit.has_toilet = edit_form.has_toilet.data
        cafe_to_edit.has_wifi = edit_form.has_wifi.data
        cafe_to_edit.can_take_calls = edit_form.can_take_calls.data
        cafe_to_edit.seats = edit_form.seats.data
        cafe_to_edit.coffee_price = edit_form.coffee_price.data

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=edit_form, is_edit=True)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
