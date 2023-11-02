from flask import Flask,render_template,flash,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired
import mysql.connector
import csv
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key no one knows"

# initializing the database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mineth:mineth123@localhost/supplychain'


mydb =mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mineth123",
    database ="supplychain")


my_cursor =mydb.cursor()


class UserForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email= StringField("Email",validators=[DataRequired()])
    password =StringField("Password",validators=[DataRequired()])
    Type_ID=StringField("Type",validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()])
    submit = SubmitField("Submit")



class Company_OrderForm(FlaskForm):
    
    quantity = IntegerField("Quantity",validators=[DataRequired()])
    User_ID = IntegerField("User ID", validators=[DataRequired()])
    Product_ID = IntegerField("Product ID", validators=[DataRequired()])
    Railway_station = StringField("Railway station", validators=[DataRequired()])
    Train_Route_ID = IntegerField("Train Route ID", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Store_OrderForm(FlaskForm):
    
    quantity = IntegerField("Quantity",validators=[DataRequired()])
    User_ID = IntegerField("User ID", validators=[DataRequired()])
    Truck_ID = IntegerField("Truck ID", validators=[DataRequired()])
    Store_ID = IntegerField("Store ID", validators=[DataRequired()])
    Product_ID = IntegerField("Product ID", validators=[DataRequired()])
    Truck_Route_ID = IntegerField("Truck Route ID", validators=[DataRequired()] )
    Driver_ID = IntegerField("Driver", validators=[DataRequired()])
    Ass_Driver_ID = IntegerField("Assistant_Driver", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Flask_Login

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def home():
    return render_template("finalhomepage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")

def contact():
    return render_template("contact.html")

@app.route("/userdash")
#@login_required
def userdash():
    return render_template("userdash.html")

@app.route("/wholedash")
@login_required
def wholedash():
    return render_template("wholedash.html")

@app.route("/retaildash")
@login_required
def retaildash():
    return render_template("retaildash.html")

@app.route("/managerdash")
#@login_required
def managerdash():
    return render_template("managerdash.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    email = None

    print('hello world')

    form = UserForm()
    
    user_email = form.email.data
    password = form.password.data

    my_cursor.execute("SELECT user_Name, User_Type "
                  "FROM users "
                  "JOIN user_type ON users.Type_ID = user_type.Type_ID "
                  "WHERE Email = %s AND Password = %s", (user_email, password))

    user_data = my_cursor.fetchone()

    if user_data is not None:
        session['user_name'] = user_data[0]  # Store user's name in session
        user_id = user_data[0]
        user_type = user_data[1]  # Get user's type from the database

        user = User(user_id)  
        login_user(user)

        if user_type == 'Customers':
            return redirect(url_for("userdash"))
        elif user_type == 'Wholesaler':
            return redirect(url_for("wholedash"))
        elif user_type == 'Retailer':
            return redirect(url_for("retaildash"))
        elif user_type == 'Manager':
            return redirect(url_for("managerdash"))
        elif user_type == 'StoreManager':
            return redirect(url_for("storedash"))
    else:
        flash("Incorrect email or password. Please try again.")

    return render_template("login.html", form=form)



@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("home"))


@app.route("/info",methods=["GET"])
@login_required
def userinfo(): 
    my_cursor.execute("SELECT * FROM users ORDER BY date_added")
    our_users = my_cursor.fetchall()
    return render_template("userdata.html",our_users=our_users)

@app.route("/report",methods=["GET"])
@login_required
def report():
    my_cursor.execute("SELECT product.Name, SUM(orders.Quantity) AS total_quantity "
                     "FROM orders "
                     "INNER JOIN product ON product.Product_ID = orders.Product_ID "
                     "GROUP BY product.Name "
                     "ORDER BY total_quantity DESC;")

    product_data = my_cursor.fetchall()
    my_cursor.execute("SELECT driver.Name, SUM(driver_roster.working_hrs) AS total_hrs_worked "
                  "FROM driver "
                  "INNER JOIN driver_roster ON driver.Main_Driver_ID = driver_roster.Driver_ID "
                  "GROUP BY driver.Name "
                  "ORDER BY total_hrs_worked DESC;")

    driver_data = my_cursor.fetchall()

    my_cursor.execute("SELECT Truck_ID, SUM(working_hrs) AS total_working_hrs "
                    "FROM driver_roster " 
                    "GROUP BY Truck_ID "
                    "ORDER BY total_working_hrs DESC;")


    truck_data = my_cursor.fetchall()

    my_cursor.execute("SELECT Unit_price, Name, Unit_capacity FROM Product")

    report_data = my_cursor.fetchall()
    return render_template("report.html",product_data=product_data,driver_data=driver_data,truck_data =truck_data, report_data = report_data  )








@app.route("/register", methods=['GET', 'POST'])
def register():
    email = None
    name = None
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        Type_ID = form.Type_ID.data
        address = form.address.data
        my_cursor.execute("SELECT user_ID FROM users WHERE Email = %s", (email,))
        existing_user = my_cursor.fetchone()
        if not existing_user:
            my_cursor.execute("INSERT INTO users(Email, password, user_Name, Type_ID, address, date_added) VALUES (%s, %s, %s, %s, %s, %s)", (email, password, name, Type_ID, address, datetime.utcnow()))
            mydb.commit()
            flash("User registered successfully!")
            return redirect(url_for("home"))  # Redirect to the home page after successful registration
        else:
            flash("User with this email already exists")
        form.email.data = ''
        form.password.data = ''
        form.name.data = ''
        form.Type_ID.data = ''
        form.address.data = ''

    return render_template("signin.html", form=form, email=email)

        
       
       



@app.route("/company_order", methods=['GET', 'POST'])
#@login_required
def company_order():

    form = Company_OrderForm()
    if form.validate_on_submit():
        User_ID = form.User_ID.data
        Product_ID = form.Product_ID.data
        Railway_station = form.Railway_station.data
        Train_Route_ID = form.Train_Route_ID.data
        Quantity = form.quantity.data

        current_datetime = datetime.utcnow()
        
        
        
        my_cursor.execute("INSERT INTO orders(User_ID, Product_ID, Railway_station,Train_Route_ID, Quantity, Date) VALUES (%s, %s, %s, %s, %s, %s)",
                            (User_ID, Product_ID, Railway_station,Train_Route_ID, Quantity, current_datetime))
        mydb.commit()
        flash("Order added successfully!")

        form.User_ID.data = ''
        form.Product_ID.data = ''
        form.Railway_station.data = ''
        form.Train_Route_ID.data= ''
        form.quantity.data = ''


        
        return redirect(url_for("home"))  # Redirect to the home page after successful registration
        
        
    return render_template("company_order.html", form=form)

@app.route("/newreport")
def newreport():
    return render_template("newreport.html")


@app.route("/store_order", methods=['GET', 'POST'])
@login_required
def store_order():
    form = Store_OrderForm()
    
    if form.validate_on_submit():
        User_ID = form.User_ID.data
        Truck_ID = form.Truck_ID.data
        Store_ID = form.Store_ID.data
        Product_ID = form.Product_ID.data
        Driver_ID = form.Driver_ID.data  # Assuming you have this field in your form
        Ass_Driver_ID = form.Ass_Driver_ID.data  # Assuming you have this field in your form
        Truck_Route_ID = form.Truck_Route_ID.data
        Quantity = form.quantity.data

        current_datetime = datetime.utcnow()
        
        my_cursor.execute("INSERT INTO store_orders (User_ID, Truck_ID, Store_ID, Product_ID, Driver_ID, Ass_Driver_ID, Truck_Route_ID, Quantity, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (User_ID, Truck_ID, Store_ID, Product_ID, Driver_ID, Ass_Driver_ID, Truck_Route_ID, Quantity, current_datetime))
        mydb.commit()
        flash("Order added successfully!")

        form.User_ID.data = ''
        form.Truck_ID.data = ''
        form.Store_ID.data = ''
        form.Product_ID.data = ''
        form.Driver_ID.data = ''
        form.Ass_Driver_ID.data = ''
        form.Truck_Route_ID.data = ''
        form.quantity.data = ''

        return redirect(url_for("home"))  # Redirect to the home page after successful registration
        
    return render_template("store_order.html", form=form)

# @app.route("/user_profile", methods=['GET', 'POST'])
# def user_profile():

class OrderForm(FlaskForm):
    product_name = StringField("Product_Name",validators=[DataRequired()])
    
    quantity = IntegerField("Quantity",validators=[DataRequired()])
    Route = StringField("Route",validators=[DataRequired()])
    User_ID = IntegerField("User_ID",validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/user_order",methods =['GET','POST'])
#@login_required
def user_order():
    # product_name = None
    form = OrderForm()
    report_data = []
    

    my_cursor.execute("SELECT Unit_price, Name, Unit_capacity FROM Product")

    product_names = my_cursor.fetchall()  

    my_cursor.execute("SELECT Origin FROM truck_route")

    route_data = my_cursor.fetchall()
    # product_names = [row[1] for row in my_cursor.fetchall()]

    if form.validate_on_submit():
        product_name = form.product_name.data
        
        quantity = form.quantity.data
        current_datetime = datetime.utcnow()

        # Insert the order into the database

        
       
        my_cursor.execute("INSERT INTO user_order(product_name,quantity,Route,User_ID,date_added) VALUES (%s, %s, %s, %s, %s )",
                            (product_name,quantity,Route,User_ID, current_datetime))
        mydb.commit()
        flash("Order added successfully!")

        
        

        form.product_name.data = ''
        
        form.quantity.data = ''

        

        


        return render_template("receipt.html",form=form,report_data=product_names, route_data = route_data)

    

    return render_template("orderpage.html", form=form,report_data=product_names, route_data = route_data )