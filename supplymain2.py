from flask import Flask,render_template,flash,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import mysql.connector
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key no one knows"

# initializing the database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mineth:mineth123@localhost/new_users'

mydb =mysql.connector.connect(
    host = "localhost",
    user = "mineth",
    passwd = "mineth123",
    database ="new_users")


my_cursor =mydb.cursor()



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
        email = form.email.data
        my_cursor.execute("SELECT id FROM Users WHERE email =%s",(email,))
        existing_user = my_cursor.fetchone()
        if not existing_user:
            user_name = form.name.data
            my_cursor.execute("INSERT INTO Users(name,email,date_added) VALUES(%s, %s, %s)",(user_name, email, datetime.utcnow()))
            mydb.commit()
            name = user_name
            flash("User added successfully!")
        else:
            flash("Users already exists")
        form.name.data = ''
        form.email.data = ''
        
    my_cursor.execute("SELECT * FROM Users ORDER BY date_added")
    our_users =my_cursor.fetchall()
    return render_template("login.html",form = form, name = name, our_users= our_users)

@app.route("/info")
def userinfo(): 
    my_cursor.execute("SELECT * FROM Users ORDER BY date_added")
    our_users = my_cursor.fetchall()
    return render_template("userdata.html",our_users=our_users)


@app.route("/order",methods =['GET','POST'])
def order():
    product_name = None
    form = OrderForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        route = form.route.data
        quantity = form.quantity.data
        address = form.address.data
        my_cursor.execute("INSERT INTO Orders(product_name,route,quantity,address,date_added) VALUES (%s, %s, %s, %s, %s)",(product_name, route,quantity, address, datetime.utcnow()))
        mydb.commit()

        form.product_name.data = ''
        form.route.data = ''
        form.quantity.data =''
        form.address.data =''

        flash("Order added successfully!")
    my_cursor.execute("SELECT * FROM Orders ORDER BY date_added")
    order_users = my_cursor.fetchall()
    return render_template("orderpage.html",form = form, product_name = product_name, order_users= order_users)