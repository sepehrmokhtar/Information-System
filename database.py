import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='localhost',       # MySQL host
    user='',   # MySQL username
    password='',  # MySQL password
)

# Create a cursor object
cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS ehr")
connection.commit()

connection = mysql.connector.connect(
    host='localhost',       # MySQL host
    user='',            # MySQL username
    password='',            # MySQL password
    database='ehr'          # Connect to the 'ehr' database
)

# Create a new cursor object to execute further SQL commands
cursor = connection.cursor()

# Write SQL queries to create the tables
Doctor = """
CREATE TABLE DOCTORS (
    doctor_id INT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(100),
    specialization VARCHAR(100),
    company VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(15),
    PRIMARY KEY (doctor_id)
);
"""

Patient = """
CREATE TABLE PATIENTS (
    patient_id INT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(100),
    PRIMARY KEY (patient_id)
);
"""

# Execute the queries
cursor.execute(Doctor)
cursor.execute(Patient)
connection.commit()
# Close the cursor and the connection
cursor.close()
connection.close()

print("Tables created")
