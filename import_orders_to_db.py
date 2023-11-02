import mysql.connector
import pandas as pd
from datetime import datetime

# Database configuration
db_config = {
    "host": "localhost",
    "user": "mineth",
    "passwd": "mineth123",
    "database": "new_users",
}

# Path to the CSV file
csv_file_path = 'static/files/orderlist.csv'

# Connect to the database
mydb = mysql.connector.connect(**db_config)
my_cursor = mydb.cursor()

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Iterate through the CSV data and insert records into the Users table
for _, row in df.iterrows():
    product_name = row['product_name']
    route = row['route']
    quantity = row['quantity']
    Address = row['Address']
    my_cursor.execute("INSERT INTO Orders (product_name, route, quantity, Address) VALUES (%s, %s, %s, %s)",
                      (product_name, route, quantity, Address))
    mydb.commit()

# Close the database connection
my_cursor.close()
mydb.close()
