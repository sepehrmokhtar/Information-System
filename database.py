import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='sql7.freesqldatabase.com',       # MySQL host
    user='sql7741129',   # MySQL username
    password='XUQ35MWg9D',  # MySQL password
    database='sql7741129'   # Connect to the database
)

# Create a cursor object
cursor = connection.cursor()

# Write SQL queries to create the tables
Doctor = """
CREATE TABLE doctors (
    doctor_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialization VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(15),
    PRIMARY KEY (doctor_id)
);
"""

Patient = """
CREATE TABLE patients (
    patient_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(100)
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
