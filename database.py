import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='sql7.freesqldatabase.com',       # MySQL host
    user='sql7746745',   # MySQL username
    password='qVMtw78yWQ',  # MySQL password
    database='sql7746745'   # Connect to the database
)

# Create a cursor object
cursor = connection.cursor()

# Write SQL queries to create the tables
Doctor = """
CREATE TABLE doctors (
    doctor_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    organization VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    PRIMARY KEY (doctor_id)
);
"""

Patient = """
CREATE TABLE patients (
    patient_id INT NOT NULL AUTO_INCREMENT, 
    first_name VARCHAR(100) NOT NULL,          
    last_name VARCHAR(100) NOT NULL,           
    email VARCHAR(100) NOT NULL UNIQUE,        
    address VARCHAR(100) NOT NULL,             
    gender VARCHAR(100) NOT NULL,              
    age INT NOT NULL,                          
    race VARCHAR(100) NOT NULL,               
    insurance_number CHAR(20) NOT NULL,        
    phone_number VARCHAR(100) NOT NULL,        
    admission_date DATE NOT NULL,              
    responsible_doctor VARCHAR(100) NOT NULL,
    family_status VARCHAR(100) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    PRIMARY KEY (patient_id)
);
"""

PatientMedInfo = """
CREATE TABLE PatientMedInfo (                           
    patient_id INT NOT NULL,                       
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    heart_rate INT NOT NULL,
    respiratory_rate INT NOT NULL,
    core_temperature FLOAT NOT NULL,
    blood_oxygen INT NOT NULL,
    blood_pressure INT NOT NULL,
    disease_history TEXT,
    family_history TEXT,
    immunization_stats TEXT,
    food_allergies VARCHAR(200),
    medication_allergies VARCHAR(200),
    other_allergies VARCHAR(200),
    smoking_history BOOLEAN NOT NULL,
    alcoholic BOOLEAN NOT NULL,
    current_med_name VARCHAR(200),
    current_med_dosage VARCHAR(100),
    current_med_frequency VARCHAR(100),
    past_medication VARCHAR(200),
    wbc FLOAT,
    rbc FLOAT,
    hco3 FLOAT,
    glucose FLOAT,
    chief_complaint TEXT,
    soap_notes TEXT,
    ros TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
"""

# Execute the queries
cursor.execute(Doctor)
cursor.execute(Patient)
cursor.execute(PatientMedInfo)

connection.commit()
# Close the cursor and the connection
cursor.close()
connection.close()

print("Tables created")
