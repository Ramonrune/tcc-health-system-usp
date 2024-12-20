from sqlalchemy import Column, String, DECIMAL, Date, DateTime, SmallInteger, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db
from app.appointment.model import Appointment
from app.disease.model import Disease
from app.exam.model import Exam
from app.medication.model import Medication


class Patient(db.Model):
    __tablename__ = "patient"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=True)
    height = Column(Integer, nullable=True)
    gender = Column(String(1), nullable=True)
    birth_date = Column(Date, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(14), nullable=False)
    blood_type = Column(String(3), nullable=True)
    smookes = Column(SmallInteger, nullable=True)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan", viewonly=True, lazy=True)
    diseases = relationship("Disease", secondary="patient_disease", back_populates="patients",  viewonly=True, lazy=True)
    exams = relationship("Exam", back_populates="patient",  viewonly=True,  lazy=True)
    attends = relationship("Attend", back_populates="patient",  viewonly=True,  lazy=True)
    medications = relationship("Medication", secondary="patient_medication", back_populates="patients", viewonly=True, lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weight": str(self.weight),
            "height": str(self.height),
            "gender": self.gender,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "cpf": self.cpf,
            "email": self.email,
            "phone": self.phone,
            "blood_type": self.blood_type,
            "smookes": bool(self.smookes), 
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }
        
        
class Attend(db.Model):
    __tablename__ = "attend"

    id = Column(String(36),  primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(String(36), ForeignKey("patient.id", ondelete="CASCADE"),  nullable=False)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="attends")
    patient = relationship("Patient", back_populates="attends")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }
