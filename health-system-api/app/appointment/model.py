from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db

class Appointment(db.Model):
    __tablename__ = "appointment"

    appointment_id = Column(String(36),  primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(String(36), ForeignKey("patient.id", ondelete="CASCADE"),  nullable=False)
    annotation =  Column(Text, nullable=True)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "annotation": self.annotation,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }
