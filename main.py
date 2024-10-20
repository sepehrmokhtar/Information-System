# MySQL Datatbase created in database.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Sina:1111@localhost:3306/ehr' # install the pymysql. Created MySQL database runs on locahost port 3306
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "12345678910"

db = SQLAlchemy(app)

class Doctor(db.Model):

    __tablename__ = 'doctors'

    doctor_id = db.Column('doctor_id', db.Integer, primary_key=True) # Points to doctor_id in MySQL db
    full_name = db.Column('full_name', db.String(100), nullable=False)
    specialization = db.Column('specialization', db.String(100))
    company = db.Column('company', db.String(100))
    email = db.Column('email', db.String(100), nullable=False, unique=True)
    password = db.Column('password', db.String(15), nullable=False)

    def __init__(self, full_name, specialization, company, email, password):
        self.full_name = full_name
        self.specialization = specialization
        self.company = company
        self.email = email
        self.password = password


class Patient(db.Model):

    __tablename__ = 'patients'

    patient_id = db.Column('patient_id', db.Integer, primary_key=True)
    full_name = db.Column('full_name', db.String(100))

    def __init__(self, full_name):
        self.full_name = full_name


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register-doctor', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form['nm']
        specialization = request.form['spcz']
        company = request.form['cmp']
        email = request.form['eml']
        password = request.form['psw']
        if Doctor.query.filter_by(email=email).first():
            flash("Doctor already registered")
            return redirect(url_for("home"))
        else:
            doctor = Doctor(full_name, specialization, company, email, password)
            db.session.add(doctor)
            db.session.commit()
            flash("Doctor was successfully registered.")
            return redirect(url_for("home"))
    return render_template("Doctor-Registration.html")


@app.route('/about-us')
def about():
    return render_template('about-us.html')


@app.route('/info')
def info():
    return render_template('info.html')


'''
@app.route('/login', methods=["GET", "POST"]) # Sessions to be done here.
def login():
    #TODO

@app.route('/view')
def view():
     #TODO: Will view the patient database
'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure this is inside the app context, and before everything the tables are created.
    app.run(debug=True)
