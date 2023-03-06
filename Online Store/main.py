from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, NewItemForm, EditItemForm
from flask_gravatar import Gravatar
from datetime import datetime
import stripe

BASE_URL = "http://127.0.0.1:5000"

stripe.api_key = 'sk_test_51MY3duITN1T2i86gfDeNuivL66fodFzzsPPyqGP2moMBf1HrseB9Ylf3VNCv9yP83PmNh7ZwsJN0XMEcMfLRnMOr00eamAqPwD'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrettodolistpassword1'
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


# connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# configure DB tables
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    cart_item = relationship("Cart", back_populates="customer")
    order_item = relationship("Order", back_populates="customer")
    phone = db.Column(db.String(15))
    b_day = db.Column(db.Date, nullable=False)

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    barcode = db.Column(db.String(100), unique=True)
    quantity = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    img_url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Text, nullable=False)
    discount = db.Column(db.Integer)
    show = db.Column(db.Boolean)
    cart_item = relationship("Cart", back_populates="item")
    details = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(250), nullable=False)

class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item = relationship("Item", back_populates="cart_item") 
    item_count = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = relationship("User", back_populates="cart_item") 
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    order = relationship("Order", back_populates="order_item") 

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total = db.column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = relationship("User", back_populates="order_item") 
    order_item = relationship("Cart", back_populates="order")

with app.app_context():
    db.create_all()

# admin setting
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 2:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.template_filter()
def currencyFormat(value):
    convert = float(value.split("$")[1])
    return convert


# all pages
@app.route('/', methods=["GET", "POST"])
def home():
    # get first 3 items not out of stock and with the current highest discount 
    try:
        items = Item.query.filter(Item.quantity>0).order_by(Item.discount.desc())[0:3]
    except:
        items = []
    # get number of items in cart
    try:
        cart_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN").count()
    except:
        cart_items = []
    return render_template("home.html", promotion_items=items, cart_items=cart_items)


@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hash_and_salted_password,
            phone=form.phone.data,
            b_day=form.b_day.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)
 

@app.route('/cart', methods=["GET", "POST"])
def cart():
    pending_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN")
    total = 0
    total_discount = 0
    subtotal = 0
    for item in pending_items:
        price = currencyFormat(item.item.price)
        subtotal += (price * item.item_count)
        total_discount += (price * item.item.discount * item.item_count)
    total = subtotal - total_discount
    return render_template("cart.html", order=pending_items, total=total, subtotal=subtotal, discount=total_discount)    


@app.route('/add-to-cart/<int:item_id>/', methods=["POST", "GET"])
def add_to_cart(item_id):
    count = int(request.form.get('count'))  

    selected_item = Item.query.filter_by(id=item_id).first()
    
    previous_order = Cart.query.filter_by(item=selected_item).filter_by(status="OPEN").first()
    
    # item is already in cart
    if previous_order:
        previous_order.item_count += count
    # item is not in cart
    else:        
        new_order = Cart(
            status = "OPEN",
            item = selected_item,
            item_count = count,
            customer = current_user,      
        )
        db.session.add(new_order)

    db.session.commit()

    return redirect(url_for("estore"))   


@app.route('/update-cart/<int:order_id>/', methods=["POST"])
def update_cart(order_id):
    count = int(request.form.get('count'))    

    previous_order = Cart.query.get(order_id)
    previous_order.item_count = count  

    db.session.commit()

    return redirect(url_for("cart"))  


@app.route('/remove-from-cart/<int:item_id>/', methods=["GET", "POST"])
def remove_from_cart(item_id):
    item_to_remove = Cart.query.get(item_id)
    db.session.delete(item_to_remove)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/estore', methods=["GET", "POST"])
def estore():
    items = Item.query.all()
    # get number of items in cart
    cart_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN").count()
    return render_template("estore.html", all_items=items, cart_items=cart_items)   


@app.route('/item/<int:item_id>', methods=["GET", "POST"])
def item(item_id):
    item = Item.query.get(item_id)
    # get related items to selected item by category
    related_items = Item.query.filter_by(category=item.category)[0:4]
    # get number of items in cart
    cart_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN").count()
    return render_template("item.html", item=item, related_items=related_items, cart_items=cart_items)  

@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    print(url_for('success'))
    # get cart total cost
    pending_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN")
    total = 0
    total_discount = 0
    subtotal = 0

    for item in pending_items:
        price = currencyFormat(item.item.price)
        subtotal += (price * item.item_count)
        total_discount += (price * item.item.discount * item.item_count)

    total = "{:.0f}".format((subtotal - total_discount) * 100) # checkout units of Cents

    # create stipe product and price with cart cost
    product = stripe.Product.create(name="Cart", images=["https://img.icons8.com/bubbles/256/shopping-cart.png"])
    price = stripe.Price.create(product=product.id, unit_amount=total, currency="usd")

    # create stripe checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url = BASE_URL + '/checkout-success',
            cancel_url = BASE_URL + '/checkout-cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route('/checkout-success', methods=["GET", "POST"])
def success():
    # update paid order to orders table
    new_order = Order(
        date = datetime.now(),
        total = 0,
        customer = current_user,
    )
    db.session.add(new_order)
    db.session.commit()

    total = 0
    total_discount = 0
    subtotal = 0
    # update cart items with order number and status
    paid_items = Cart.query.filter_by(customer=current_user).filter_by(status="OPEN")
    for item in paid_items:
        # update item quantity in stock - items table
        item.item.quantity -= item.item_count
        # update cart status
        item.status = "PAID"
        item.order = new_order
        db.session.commit()

        price = currencyFormat(item.item.price)
        subtotal += (price * item.item_count)
        total_discount += (price * item.item.discount * item.item_count)

    total = "{:.0f}".format(subtotal - total_discount) 
    new_order.total = total
    db.session.commit()

    return render_template("success.html")


@app.route('/checkout-fail', methods=["GET", "POST"])
def cancel():
    return render_template("cancel.html")

@app.route('/new-item', methods=["GET", "POST"])
@admin_only
def new_item():
    form = NewItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name = form.name.data,
            barcode = form.barcode.data,
            quantity = form.quantity.data,
            rating = form.rating.data,
            img_url = form.img_url.data,
            description = form.description.data,
            details = form.details.data,
            category = form.category.data,
            price = form.price.data,
            show = form.show.data,
            discount = form.discount.data
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('estore'))
    return render_template("new_item.html", form=form)    


@app.route('/edit-item/<int:item_id>', methods=["GET", "POST"])
@admin_only
def edit_item(item_id):
    item = Item.query.get(item_id)
    edit_form = EditItemForm(
            name = item.name,
            barcode = item.barcode,
            quantity = item.quantity,
            rating = item.rating,
            img_url = item.img_url,
            description = item.description,
            details = item.details,
            category = item.category,
            price = item.price,
            show = item.show,
            discount = item.discount
    )

    if edit_form.validate_on_submit():
        item.name = edit_form.name.data
        item.barcode = edit_form.barcode.data
        item.quantity = edit_form.quantity.data
        item.rating = edit_form.rating.data
        item.img_url = edit_form.img_url.data
        item.description = edit_form.description.data
        item.details = edit_form.details.data
        item.category = edit_form.category.data
        item.price = edit_form.price.data
        item.show = edit_form.show.data
        item.discount = edit_form.discount.data
        db.session.commit()
        return redirect(url_for('estore'))

    return render_template("edit_item.html", form=edit_form)   

@app.route('/admin', methods=["GET", "POST"])
@admin_only
def admin():
    users = User.query.all()
    missing_items = Item.query.filter_by(quantity=0)
    all_items = Item.query.all()
    orders = Order.query.order_by(Order.date.desc()).all()
    carts = Cart.query.all()
    return render_template("admin.html", users=users, missing_items=missing_items, orders=orders, carts=carts, all_items=all_items)   

@app.route('/delete-user/<int:user_id>')
@admin_only
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))  

if __name__ == "__main__":
    app.run(debug=True)
