from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db


class Disease(db.Model):
    __tablename__ = "disease"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(255), unique=True, nullable=False)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    patients = relationship("Patient", secondary="patient_disease", back_populates="diseases", viewonly=True, lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }
        
class PatientDisease(db.Model):
    __tablename__ = "patient_disease"

    id = Column(String(36), primary_key=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patient.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    disease_id = Column(String(36), ForeignKey("disease.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    note = Column(Text, nullable=True)
    date_entered = Column(DateTime, nullable=False, default=func.now())
    
    disease = relationship("Disease", backref="patient_disease")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "disease_id": self.disease_id,
            "note": self.note,
            "disease": self.disease.to_dict(),
            "date_entered": self.date_entered.strftime("%d/%m/%Y")
        }