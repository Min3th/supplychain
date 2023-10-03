from flask import Flask,render_template,flash,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key no one knows"

# initializing the database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mineth:mineth123@localhost/new_users'


db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable =False)
    email =db.Column(db.String(100), nullable =False,unique = True)
    date_added =db.Column(db.DateTime,default = datetime.utcnow)

    # Creating a string

    def __repr__(self):
        return '<Name %r>' % self.name

class Orders(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    product_name = db.Column(db.String(100), nullable =False)
    route =db.Column(db.String(100), nullable =False,unique = True)
    quantity=db.Column(db.Integer, nullable =False,unique = True)
    address=db.Column(db.String(100), nullable =False,unique = True)
    date_added =db.Column(db.DateTime,default = datetime.utcnow)

class UserForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email= StringField("Email",validators=[DataRequired()])
    #user_type=StringField("Type",validators=[DataRequired()])
    submit = SubmitField("Submit")

class OrderForm(FlaskForm):
    product_name = StringField("Product_Name",validators=[DataRequired()])
    route= StringField("Route",validators=[DataRequired()])
    quantity=StringField("Quantity",validators=[DataRequired()])
    address =StringField("Address",validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/login",methods =['GET','POST'])
def login():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("login.html",form = form, name = name, our_users= our_users)

@app.route("/info")
def userinfo():
    our_users = Users.query.order_by(Users.date_added)
    return render_template("userdata.html",our_users=our_users)


@app.route("/order",methods =['GET','POST'])
def order():
    product_name = None
    form = OrderForm()
    if form.validate_on_submit():
        order = Orders(product_name=form.product_name.data,route=form.route.data,quantity=form.quantity.data,address=form.address.data)
        db.session.add(order)
        db.session.commit()
        product_name = form.product_name.data
        form.product_name.data = ''
        form.route.data = ''
        form.quantity.data =''
        form.address.data =''
        flash("Order added successfully!")
    order_users = Orders.query.order_by(Orders.date_added)
    return render_template("orderpage.html",form = form, product_name = product_name, order_users= order_users)