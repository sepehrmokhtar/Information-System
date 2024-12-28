# MySQL Datatbase created in database.py
import json
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash # Used to hash passwords stored in database.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql7746745:qVMtw78yWQ@sql7.freesqldatabase.com/sql7746745' # install the pymysql. Created MySQL database runs on localhost port 3306
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "12345678910" # In order to safely store session cookies.
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)


class Doctor(db.Model):

    __tablename__ = 'doctors'

    doctor_id = db.Column('doctor_id', db.Integer, primary_key=True) # Points to doctor_id in MySQL db
    first_name = db.Column('first_name', db.String(100), nullable=False)
    last_name = db.Column('last_name', db.String(100), nullable=False)
    specialization = db.Column('specialization', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), nullable=False, unique=True)
    password = db.Column('password', db.String(200))
    phone_number = db.Column('phone_number', db.String(20))
    organization = db.Column('organization', db.String(20))
    address = db.Column('address', db.String(100), nullable=False)

    def __init__(self, first_name, last_name, specialization, email, password, phone_number, organization, address):
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.organization = organization
        self.address = address


class Patient(db.Model):

    __tablename__ = 'patients'

    patient_id = db.Column('patient_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100), nullable=False)
    last_name = db.Column('last_name', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), nullable=False, unique=True)
    address = db.Column('address', db.String(100), nullable=False)
    gender = db.Column('gender', db.String(100), nullable=False)
    age = db.Column('age', db.Integer, nullable=False)
    race = db.Column('race', db.String(100), nullable=False)
    insurance_number = db.Column('insurance_number', db.String(20), nullable=False)
    phone_number = db.Column('phone_number', db.String(100), nullable=False)
    admission_date = db.Column('admission_date', db.Date, nullable=False)
    responsible_doctor = db.Column('responsible_doctor', db.String(100), nullable=False)
    family_status = db.Column('family_status', db.String(100), nullable=False)
    occupation = db.Column('occupation', db.String(100), nullable=False)

    def __init__(self, first_name, last_name, email, address, gender, age, race, insurance_number,
                 phone_number, admission_date, responsible_doctor, family_status, occupation):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.gender = gender
        self.age = age
        self.race = race
        self.insurance_number = insurance_number
        self.phone_number = phone_number
        self.admission_date = admission_date
        self.responsible_doctor = responsible_doctor
        self.family_status = family_status
        self.occupation = occupation


class PatientMedInfo(db.Model):

    __tablename__ = 'PatientMedInfo'

    patient_med_info_id = db.Column('patient_med_info_id', db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    heart_rate = db.Column('heart_rate', db.Integer, nullable=False)
    respiratory_rate = db.Column('respiratory_rate', db.Integer, nullable=False)
    core_temperature = db.Column('temperature', db.Float, nullable=False)
    blood_oxygen = db.Column('blood_oxygen', db.Integer, nullable=False)
    blood_pressure = db.Column('blood_pressure', db.Integer, nullable=False)
    disease_history = db.Column('disease_history', db.Text, nullable=True)
    family_history = db.Column('family_history', db.Text, nullable=True)
    immunization_stats = db.Column('immunization_stats', db.Text, nullable=True)
    food_allergies = db.Column('food_allergies', db.String(200), nullable=True)
    medication_allergies = db.Column('medication_allergies', db.String(200), nullable=True)
    other_allergies = db.Column('other_allergies', db.String(200), nullable=True)
    smoking_history = db.Column('smoking_history', db.Boolean, nullable=False)
    alcoholic = db.Column('alcoholic', db.Boolean, nullable=False)
    current_med_name = db.Column('current_med_name', db.String(200), nullable=True)
    current_med_dosage = db.Column('current_med_dosage', db.String(100), nullable=True)
    current_med_frequency = db.Column('current_med_frequency', db.String(100), nullable=True)
    past_medication = db.Column('past_medication', db.String(200), nullable=True)
    wbc = db.Column('wbc', db.Float, nullable=True)
    rbc = db.Column('rbc', db.Float, nullable=True)
    hco3 = db.Column('hco3', db.Float, nullable=True)
    glucose = db.Column('glucose', db.Float, nullable=True)
    chief_complaint = db.Column('chief_complaint', db.Text, nullable=True)
    soap_notes = db.Column('soap_notes', db.Text, nullable=True)
    ros = db.Column('ros', db.Text, nullable=True)

    def __init__(self, patient_med_info_id, patient_id, height, weight, heart_rate, respiratory_rate, core_temperature,
                 blood_oxygen, blood_pressure, disease_history=None, family_history=None,
                 immunization_stats=None, food_allergies=None, medication_allergies=None,
                 other_allergies=None, smoking_history=False, alcoholic=False, current_med_name=None,
                 current_med_dosage=None, current_med_frequency=None, past_medication=None,
                 wbc=None, rbc=None, hco3=None, glucose=None, chief_complaint=None, soap_notes=None,
                 ros=None):
        self.patient_med_info_id = patient_med_info_id
        self.patient_id = patient_id
        self.height = height
        self.weight = weight
        self.heart_rate = heart_rate
        self.respiratory_rate = respiratory_rate
        self.core_temperature = core_temperature
        self.blood_oxygen = blood_oxygen
        self.blood_pressure = blood_pressure
        self.disease_history = disease_history
        self.family_history = family_history
        self.immunization_stats = immunization_stats
        self.food_allergies = food_allergies
        self.medication_allergies = medication_allergies
        self.other_allergies = other_allergies
        self.smoking_history = smoking_history
        self.alcoholic = alcoholic
        self.current_med_name = current_med_name
        self.current_med_dosage = current_med_dosage
        self.current_med_frequency = current_med_frequency
        self.past_medication = past_medication
        self.wbc = wbc
        self.rbc = rbc
        self.hco3 = hco3
        self.glucose = glucose
        self.chief_complaint = chief_complaint
        self.soap_notes = soap_notes
        self.ros = ros


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register-doctor', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        specialization = request.form['specialization']
        phone_number = request.form['phone_number']
        organization = request.form['organization']
        address = request.form['address']
        email = request.form['email'].strip().lower()  # Normalize email
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Default is PBKDF2-SHA256
        if Doctor.query.filter_by(email=email).first():
            flash("Doctor is already registered.")
            return redirect(url_for("home"))
        else:
            doctor = Doctor(first_name, last_name, specialization, email, hashed_password, phone_number, organization, address)
            try:
                db.session.add(doctor)
                db.session.commit()
                flash("Doctor was successfully registered. Please login.")
                return redirect(url_for("home"))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while registering: {str(e)}")
                return redirect(url_for("home"))
    return render_template("register-doctor.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get('email'):
        flash('Already logged in!')
        return redirect(url_for('dashboard', last_name=session.get('last_name')))

    if request.method == "POST":
        email = request.form['email'].strip().lower()  # Normalize the input email
        password = request.form['password']
        found_doctor = Doctor.query.filter_by(email=email).first()
        if found_doctor and check_password_hash(found_doctor.password, password):
            session.permanent = True
            session['email'] = email
            session['last_name'] = found_doctor.last_name
            flash("Login successful!")
            return redirect(url_for("dashboard", last_name=found_doctor.last_name))
        else:
            flash("Login failed. Please check your credentials or make sure you are registered.")

    return render_template("login-page.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.")
    return redirect(url_for("home"))


@app.route('/dashboard/<last_name>')
def dashboard(last_name):
    if not session.get('email'):
        flash("In order to access the dashboard you need to login.")
        return redirect(url_for('login'))

    return render_template("dashboard.html", last_name=last_name)


@app.route('/dashboard/add-patient', methods=["GET", "POST"])
def add_patient():
    if not session.get('email'):
        flash("In order to add patient and access your dashboard you need to login.")
        return redirect(url_for('login'))

    if request.method == "POST":
        # Direct Information
        doctor_email = request.form['doctor_email']
        admission_date = request.form['admission-date']
        firstname = request.form['first-name']
        lastname = request.form['last-name']
        patient_email = request.form['email']
        address = request.form['address']
        insurance_number = request.form['insurance-number']
        phone_number = request.form['phone-number']

        # Demographics
        gender = request.form['gender']
        race = request.form['race']
        age = request.form['age']
        family_status = request.form['family-status']
        occupation = request.form['occupation']
        height = request.form['height']
        weight = request.form['weight']

        # Vital Signs
        core_temperature = request.form['core-temp']
        heart_rate = request.form['heart-rate']
        respiratory_rate = request.form['respiratory-rate']
        blood_oxygen = request.form['blood-oxygen']
        blood_pressure = request.form['blood-pressure']

        # Medical History
        disease_history = request.form['disease-history']
        family_history = request.form['family-history']
        immunization_status = request.form.getlist('immunization-status')
        food_allergies = request.form['food-allergy']
        medication_allergies = request.form['medication-allergy']
        other_allergies = request.form['other-allergy']
        smoking_history = request.form['smoking-history']
        alcoholic = request.form['alcohol-history']
        current_med_name = request.form['current_med_name']
        current_med_dosage = request.form['current_med_dosage']
        current_med_frequency = request.form['current_med_frequency']
        past_medication = request.form['past-medication']
        wbc = request.form['wbc']
        rbc = request.form['rbc']
        hco3 = request.form['hco3']
        glucose = request.form['glucose']

        # History of Present Illness
        chief_complaint = request.form['chief-complaint']
        soap_notes = request.form['soap-notes']
        ros = request.form['ros']

        json_stored_immunization_status = json.dumps(immunization_status)

        patient = Patient(firstname, lastname, patient_email, address, gender, age, race, insurance_number, phone_number,
                          admission_date, doctor_email, family_status, occupation)

        patient_med_info = PatientMedInfo(height, weight, core_temperature, heart_rate, respiratory_rate, blood_oxygen,
                                          blood_pressure, disease_history, family_history, json_stored_immunization_status,
                                          food_allergies, medication_allergies, other_allergies, smoking_history, alcoholic,
                                          current_med_name, current_med_dosage, current_med_frequency, past_medication, wbc,
                                          rbc, hco3, glucose, chief_complaint, soap_notes, ros)
        try:
            db.session.add(patient)
            db.session.add(patient_med_info)
            db.session.commit()
            flash("New patient was successfully added.")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while adding information: {str(e)}")
            return redirect(url_for("dashboard"))

    return render_template("add_patient.html")


@app.route('/dashboard/view-patient')
def view():
    if not session.get('email'):
        flash("In order to see patients list and access your dashboard you need to login.")
        return redirect(url_for('login'))
    
    return render_template("patient-list.html", patients=Patient.query.filter_by(responsible_doctor=session.get('email')).all())


@app.route('/dashboard/delete-patient', methods=['POST'])
def delete_patient():
    if not session.get('email'):
        flash("In order to perform this operation please login.")
        return redirect(url_for('login'))

    patient_email = request.form.get('patient_email')
    patient = Patient.query.filter_by(email=patient_email).first()

    try:
        db.session.delete(patient)
        db.session.commit()
        flash("Patient record was successfully deleted.")
        return redirect(url_for("dashboard"))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the record: {str(e)}")
        return redirect(url_for("dashboard"))


@app.route('/dashboard/update-patient', methods=["GET", "POST"])
def update_patient():
    if not session.get('email'):
        flash("In order to edit patient and access your dashboard you need to login.")
        return redirect(url_for('login'))

    email = request.form.get('patient_email')
    patient = Patient.query.filter_by(email=email).first()

    patient_id = patient.patient_id
    patient_med_info = PatientMedInfo.query.filter_by(patient_med_info_id=patient_id).first() # Reference to patient_id (foreign key)

    if request.method == "POST":
        # Direct Information
        patient.responsible_doctor = request.form['doctor-email'] if 'doctor-email' in request.form else patient.responsible_doctor
        patient.admission_date = request.form['admission-date'] if 'admission-date' in request.form else patient.admission_date
        patient.first_name = request.form['first-name'] if 'first-name' in request.form else patient.first_name
        patient.last_name = request.form['last-name'] if 'last-name' in request.form else patient.last_name
        patient.email = request.form['email'] if 'email' in request.form else patient.email
        patient.address = request.form['address'] if 'address' in request.form else patient.address
        patient.insurance_number = request.form['insurance-number'] if 'insurance-number' in request.form else patient.insurance_number
        patient.phone_number = request.form['phone-number'] if 'phone-number' in request.form else patient.phone_number

        # Demographics
        patient.gender = request.form['gender'] if 'gender' in request.form else patient.gender
        patient.race = request.form['race'] if 'race' in request.form else patient.race
        patient.age = request.form['age'] if 'age' in request.form else patient.age
        patient.family_status = request.form['family-status'] if 'family-status' in request.form else patient.family_status
        patient.occupation = request.form['occupation'] if 'occupation' in request.form else patient.occupation
        patient_med_info.height = request.form['height'] if 'height' in request.form else patient_med_info.height
        patient_med_info.weight = request.form['weight'] if 'weight' in request.form else patient_med_info.weight

        # Vital Signs
        patient_med_info.core_temperature = request.form['core-temp'] if 'core-temp' in request.form else patient_med_info.core_temperature
        patient_med_info.heart_rate = request.form['heart-rate'] if 'heart-rate' in request.form else patient_med_info.heart_rate
        patient_med_info.respiratory_rate = request.form['respiratory-rate'] if 'respiratory-rate' in request.form else patient_med_info.respiratory_rate
        patient_med_info.blood_oxygen = request.form['blood-oxygen'] if 'blood-oxygen' in request.form else patient_med_info.blood_oxygen
        patient_med_info.blood_pressure = request.form['blood-pressure'] if 'blood-pressure' in request.form else patient_med_info.blood_pressure

        # Medical History
        patient_med_info.disease_history = request.form['disease-history'] if 'disease-history' in request.form else patient_med_info.disease_history
        patient_med_info.family_history = request.form['family-history'] if 'family-history' in request.form else patient_med_info.family_history
        patient_med_info.immunization_status = request.form.getlist('immunization-status') if 'immunization-status' in request.form else patient_med_info.immunization_status
        patient_med_info.food_allergies = request.form['food-allergy'] if 'food-allergy' in request.form else patient_med_info.food_allergies
        patient_med_info.medication_allergies = request.form['medication-allergy'] if 'medication-allergy' in request.form else patient_med_info.medication_allergies
        patient_med_info.other_allergies = request.form['other-allergy'] if 'other-allergy' in request.form else patient_med_info.other_allergies
        patient_med_info.smoking_history = request.form['smoking-history'] if 'smoking-history' in request.form else patient_med_info.smoking_history
        patient_med_info.alcoholic = request.form['alcohol-history'] if 'alcohol-history' in request.form else patient_med_info.alcoholic
        patient_med_info.current_med_name = request.form['current_med_name'] if 'current_med_name' in request.form else patient_med_info.current_med_name
        patient_med_info.current_med_dosage = request.form['current_med_dosage'] if 'current_med_dosage' in request.form else patient_med_info.current_med_dosage
        patient_med_info.current_med_frequency = request.form['current_med_frequency'] if 'current_med_frequency' in request.form else patient_med_info.current_med_frequency
        patient_med_info.past_medication = request.form['past-medication'] if 'past-medication' in request.form else patient_med_info.past_medication
        patient_med_info.wbc = request.form['wbc'] if 'wbc' in request.form else patient_med_info.wbc
        patient_med_info.rbc = request.form['rbc'] if 'rbc' in request.form else patient_med_info.rbc
        patient_med_info.hco3 = request.form['hco3'] if 'hco3' in request.form else patient_med_info.hco3
        patient_med_info.glucose = request.form['glucose'] if 'glucose' in request.form else patient_med_info.glucose

        # History of Present Illness
        patient_med_info.chief_complaint = request.form['chief-complaint'] if 'chief-complaint' in request.form else patient_med_info.chief_complaint
        patient_med_info.soap_notes = request.form['soap-notes'] if 'soap-notes' in request.form else patient_med_info.soap_notes
        patient_med_info.ros = request.form['ros'] if 'ros' in request.form else patient_med_info.ros

        try:
            db.session.commit()
            flash("Patient information was successfully edited.")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the information: {str(e)}")
            return redirect(url_for("dashboard"))

    stored_immunization_status = json.loads(patient_med_info.immunization_status) # Deserialized the stored immunization_status for use in the template.

    return render_template("add_patient.html", doctor_email=patient.responsible_doctor, admission_date=patient.admission_date,
                           firstname=patient.first_name, lastname=patient.last_name, patient_email=patient.email,
                           address=patient.address, insurance_number=patient.insurance_number, phone_number=patient.phone_number,
                           gender=patient.gender, race=patient.race, age=patient.age, family_status=patient.family_status, occupation=patient.occupation,
                           height=patient_med_info.height, weight=patient_med_info.weight, core_temp=patient_med_info.core_temperature,
                           heart_rate=patient_med_info.heart_rate, respiratory_rate=patient_med_info.respiratory_rate, blood_oxygen=patient_med_info.blood_oxygen,
                           blood_pressure=patient_med_info.blood_pressure, disease_history=patient_med_info.disease_history,
                           family_history=patient_med_info.family_history, immunization_status=stored_immunization_status,
                           food_allergy=patient_med_info.food_allergies, medication_allergy=patient_med_info.medication_allergies,
                           other_allergies=patient_med_info.other_allergies, smoking_history=patient_med_info.smoking_history,
                           alcohol_history=patient_med_info.alcoholic, current_med_name=patient_med_info.current_med_name,
                           current_med_dosage=patient_med_info.current_med_dosage, current_med_frequency=patient_med_info.current_med_frequency,
                           past_medication=patient_med_info.past_medication, wbc=patient_med_info.wbc, rbc=patient_med_info.rbc,
                           hco3=patient_med_info.hco3, glucose=patient_med_info.glucose, cc=patient_med_info.chief_complaint,
                           soap=patient_med_info.soap_notes, ros=patient_med_info.ros)


@app.route('/forget-password', methods=["GET", "POST"])
def forget_password():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        new_password = request.form['new_password']
        found_doctor = Doctor.query.filter_by(email=email).first()
        if found_doctor:
            new_hashed_password = generate_password_hash(new_password)
            found_doctor.password = new_hashed_password
            db.session.commit()
            flash("New password was successfully saved. Please login again.")
            return redirect(url_for('login'))
        else:
            flash("Please make sure that the doctor is registered.")
    return render_template("forget-password.html")


@app.route('/dashboard/profile', methods=["GET", "POST"])
def profile():
    if not session.get('email'):
        flash("In order to access your profile you need to login.")
        return redirect(url_for('login'))

    doctor = Doctor.query.filter_by(email=session.get('email')).first()
    if request.method == "POST":
        doctor.first_name = request.form['firstName'] if 'firstName' in request.form else doctor.first_name
        doctor.last_name = request.form['lastName'] if 'lastName' in request.form else doctor.last_name
        doctor.specialization = request.form['specialization'] if 'specialization' in request.form else doctor.specialization
        doctor.phone_number = request.form['phone_number'] if 'phone_number' in request.form else doctor.phone_number
        doctor.organization = request.form['organization'] if 'organization' in request.form else doctor.organization
        doctor.address = request.form['address'] if 'address' in request.form else doctor.address
        try:
            db.session.commit()
            flash("Doctor information was successfully edited.")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the profile: {str(e)}")
        return redirect(url_for('profile'))

    return render_template('view-profile.html', firstname=doctor.first_name, lastname=doctor.last_name,
                           specialization=doctor.specialization, phone_number=doctor.phone_number,
                           organization=doctor.organization, address=doctor.address) # Load the existing information of the doctor into the form.


@app.route('/about-us')
def about():
    return render_template('about-us.html')


@app.route('/info')
def info():
    return render_template('info.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure this is inside the app context, and before everything the tables are created.
    app.run(debug=True)
