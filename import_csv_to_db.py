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
csv_file_path = 'static/files/usernamelist.csv'

# Connect to the database
mydb = mysql.connector.connect(**db_config)
my_cursor = mydb.cursor()

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Iterate through the CSV data and insert records into the Users table
for _, row in df.iterrows():
    user_name = row['Name']
    email = row['Email']
    my_cursor.execute("INSERT INTO Users (name, email, date_added) VALUES (%s, %s, %s)",
                      (user_name, email, datetime.utcnow()))
    mydb.commit()

# Close the database connection
my_cursor.close()
mydb.close()

print("Users imported successfully!")
