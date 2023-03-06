from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, BooleanField, DateField
from wtforms.validators import DataRequired, URL, Length, NumberRange, InputRequired
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    b_day = DateField("Birth Date", format='%Y-%m-%d', validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class NewItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    barcode = StringField("Barcode", validators=[DataRequired(), Length(min=6, max=6, message="Invalid item barcode")])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired()])
    img_url = StringField("img_url", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    details = CKEditorField("Details", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    discount = StringField("Discount", validators=[DataRequired()])
    show = BooleanField("Show", default="checked")
    submit = SubmitField("Add Item")

class EditItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    barcode = StringField("Barcode", validators=[DataRequired(), Length(min=6, max=6, message="Invalid item barcode")])
    quantity = IntegerField("Quantity", validators=[InputRequired(), NumberRange(min=0, max=999, message=None)])
    rating = FloatField("Rating", validators=[DataRequired()])
    img_url = StringField("img_url", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    details = CKEditorField("Details", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    discount = StringField("Discount", validators=[DataRequired()])
    show = BooleanField("Show", default="checked")
    submit = SubmitField("Update Item")
