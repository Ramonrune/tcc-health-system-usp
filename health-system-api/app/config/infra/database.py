import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Define a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the custom base
db = SQLAlchemy(model_class=Base)

# Configure and initialize the database
def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    db.init_app(app) 
    from app.auth.model import User
    from app.patient.model import Patient
    from app.appointment.model import Appointment
    from app.disease.model import Disease, PatientDisease
    from app.exam.model import Exam
    from app.medication.model import Medication
    
    
    #with app.app_context():
    #    from app.disease.cid10_loader import load_cid10_data
    #    from app.medication.cmed_loader import load_med_data
    

