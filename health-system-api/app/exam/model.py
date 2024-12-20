from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.infra.database import db


class Exam(db.Model):
    __tablename__ = "exam"

    id = Column(String(36), primary_key=True, nullable=False)
    date = Column(Date, nullable=False, default=func.now())
    name = Column(String(255), nullable=False)
    note = Column(Text, nullable=True)
    file_extension = Column(String(5), nullable=True)
    patient_id = Column(
        String(36), ForeignKey("patient.id", ondelete="CASCADE"), nullable=True
    )
    date_entered = Column(DateTime, nullable=False, default=func.now())

    patient = relationship("Patient", back_populates="exams")

    def to_dict(self):

        return {
            "id": self.id,
            "date": self.date.strftime("%d/%m/%Y"),
            "name": self.name,
            "note": self.note,
            "patient_id": self.patient_id,
            "file_extension": self.file_extension,
            "date_entered": (
                self.date_entered.isoformat() if self.date_entered else None
            ),
        }
