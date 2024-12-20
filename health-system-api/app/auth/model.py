from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db
from app.appointment.model import Appointment

class User(db.Model):
    __tablename__ = "user" 

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    date_entered = Column(DateTime, nullable=False, default=func.now())

    appointments = relationship("Appointment", back_populates="user", lazy=True)
    attends  = relationship("Attend", back_populates="user", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }