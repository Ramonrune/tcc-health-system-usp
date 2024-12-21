from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, func
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
    appointment_entities = relationship("AppointmentEntity", back_populates="appointment")

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "annotation": self.annotation,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }


class AppointmentEntity(db.Model):
    __tablename__ = "appointment_entity"

    id = Column(String(36),  primary_key=True)
    appointment_id = Column(String(36), ForeignKey("appointment.appointment_id", ondelete="CASCADE"), nullable=False)
    entity_text = Column(Text)
    category = Column(Text)
    sub_category = Column(Text)
    offset = Column(Integer)
    confidence = Column(Float)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    appointment = relationship("Appointment", back_populates="appointment_entities")
    #appointment_entity_relations = relationship("AppointmentEntity", back_populates="appointment_entity_relations")
    
    def to_dict(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "entity_text": self.entity_text,
            "category": self.category,
            "sub_category": self.sub_category,
            "offset": self.offset,
            "confidence": self.confidence,
            "date_entered": self.date_entered.strftime("%d/%m/%Y"),
        }


