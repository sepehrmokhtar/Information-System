# MySQL Datatbase created in database.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash # Used to hash passwords stored in database.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost:3306/ehr' # install the pymysql. Created MySQL database runs on localhost port 3306
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "12345678910" # In order to safely store session cookies.
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class Doctor(db.Model):

    __tablename__ = 'doctors'

    doctor_id = db.Column('doctor_id', db.Integer, primary_key=True) # Points to doctor_id in MySQL db
    first_name = db.Column('first_name', db.String(100), nullable=False)
    last_name = db.Column('last_name', db.String(100), nullable=False)
    specialization = db.Column('specialization', db.String(100))
    email = db.Column('email', db.String(100), nullable=False, unique=True)
    password = db.Column('password', db.String(15), nullable=False)

    def __init__(self, first_name, last_name, specialization, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
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
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        specialization = request.form['specialization']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        if Doctor.query.filter_by(email=email).first():
            flash("Doctor is already registered.")
            return redirect(url_for("home"))
        else:
            doctor = Doctor(first_name, last_name, specialization, email, hashed_password)
            try:
                db.session.add(doctor)
                db.session.commit()
                flash("Doctor was successfully registered. Please login.")
                return redirect(url_for("home"))
            except Exception:
                db.session.rollback()
                flash("An error occurred while registering. Please try again.")
                return redirect(url_for("home"))
    return render_template("Doctor-Registration.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'email' in session:
        flash('Already logged in!')
        return redirect(url_for('dashboard', last_name=session.get('last_name')))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        found_doctor = Doctor.query.filter_by(email=email).first()
        if found_doctor and check_password_hash(found_doctor.password, password):
            session.permanent = True
            session['email'] = email
            session['last_name'] = found_doctor.last_name
            flash("Login successful!")
            return redirect(url_for("dashboard", last_name=session.get('last_name')))
        else:
            flash("Login failed. Please check your credentials or make sure you are registered.")

    return render_template("login-page.html")


@app.route('/dashboard/<last_name>')
def dashboard(last_name):
    if 'email' not in session:
        flash("In order to access the dashboard you need to login.")
        return redirect(url_for('login'))
    else:
        return f"Welcome to your dashboard, {last_name}."

    return render_template("after-login.html")


@app.route('/forget-password',  methods=["GET", "POST"])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        found_doctor = Doctor.query.filter_by(email=email).first()
        if found_doctor:
            new_hashed_password = generate_password_hash(new_password, method='sha256')
            found_doctor.password = new_hashed_password
            db.session.commit()
            flash("New password was successfully saved. Please login again.")
            return redirect(url_for('login'))
    return render_template("forget-password.html")


@app.route('/about-us')
def about():
    return render_template('about-us.html')


@app.route('/info')
def info():
    return render_template('info.html')


'''
@app.route('/view')
def view():
     #TODO: Will view the patient database
'''

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure this is inside the app context, and before everything the tables are created.
    app.run(debug=True)
