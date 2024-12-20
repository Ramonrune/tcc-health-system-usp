from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db

class Medication(db.Model):
    __tablename__ = "medication"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    ean = Column(String(255), nullable=False)
    active_ingredient  = Column(String(255), nullable=False)
    lab  = Column(String(255), nullable=False)
    lab_cnpj  = Column(String(255), nullable=False)
    register  = Column(String(255), nullable=False)
    therapeutic_class  = Column(String(255), nullable=False)
    presentation  = Column(String(255), nullable=False)
    date_entered = Column(DateTime, nullable=False, default=func.now())
    
    patients = relationship("Patient", secondary="patient_medication", back_populates="medications",  viewonly=True, lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ean": self.ean,
            "active_ingredient": self.active_ingredient,
            "lab": self.lab,
            "lab_cnpj": self.lab_cnpj,
            "register": self.register,
            "therapeutic_class": self.therapeutic_class,
            "presentation": self.presentation,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }
        
class PatientMedication(db.Model):
    __tablename__ = "patient_medication"

    id = Column(String(36), primary_key=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patient.id", ondelete="CASCADE"), nullable=False)
    medication_id = Column(String(36), ForeignKey("medication.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=True)
    date_entered = Column(DateTime, nullable=False, default=func.now())
    
    
    medication = relationship("Medication", backref="patient_medication")


    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "medication_id": self.medication_id,
            "note": self.note,
            "medication": self.medication.to_dict(),
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }