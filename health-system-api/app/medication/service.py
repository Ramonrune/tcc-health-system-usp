import uuid
from sqlalchemy.exc import IntegrityError
from app.config.infra.database import db
from app.patient.model import Patient
from app.medication.dto import MedicationCreateDTO, MedicationUpdateDTO
from app.medication.model import Medication
from app.medication.model import PatientMedication
from app.util.response import Response
from sqlalchemy.orm import joinedload


class MedicationService:

    def list(self, request):
        name = request.args.get("name")
        patient_id = request.args.get("patient_id", None)
        medication_id = request.args.get("medication_id", None)
        if patient_id == None and medication_id == None:
            medications = (
                db.session.query(Medication)
                .filter(Medication.name.like(f"%{name}%"))
                .order_by(Medication.name.asc())
                .all()
            )

            medications = [medication.to_dict() for medication in medications]

            return Response.ok(
                data=medications, message="Medications sucessfully found!"
            )

        query = db.session.query(PatientMedication).join(Medication)

        if patient_id != None:
            query = query.filter(PatientMedication.patient_id == patient_id)

        if medication_id != None:
            query = query.filter(PatientMedication.medication_id == medication_id)


        query = query.order_by(PatientMedication.date_entered.desc())

        medications = query.all()

        medications = [medication.to_dict() for medication in medications]

        return Response.ok(
            data=medications, message="Patient medications sucessfully found!"
        )

    def find(self, id: str):
        medication = (
            db.session.query(PatientMedication)
            .join(Medication)
            .filter(PatientMedication.id == id)
            .first()
        )


        return Response.ok(
            data=medication.to_dict(), message="Patient medication sucessfully found!"
        )

    def register(self, body: MedicationCreateDTO):
        try:
            patient_medication = PatientMedication(
                id=str(uuid.uuid4()),
                patient_id=body.patient_id,
                medication_id=body.medication_id,
                note=body.note,
            )
            db.session.add(patient_medication)
            db.session.commit()

            return Response.created(
                data={}, message="Patient medication sucessfully registered!"
            )
        except IntegrityError:
            return Response.conflict(
                data={}, message="Patient or medication don't exist!"
            )

    def update(self, id: str, body: MedicationUpdateDTO):

        patient_medication = (
            db.session.query(PatientMedication).filter_by(id=id).first()
        )

        if patient_medication == None:
            return Response.not_found(data={}, message="Patient medication not found!")

        patient_medication.medication_id = body.medication_id
        patient_medication.note = body.note

        db.session.commit()

        return Response.ok(data={}, message="Patient medication sucessfully updated!")

    def delete(self, id: str):

        patient_medication = (
            db.session.query(PatientMedication).filter_by(id=id).first()
        )

        if patient_medication == None:
            return Response.not_found(data={}, message="Patient medication not found!")

        db.session.delete(patient_medication)

        db.session.commit()

        return Response.ok(data={}, message="Patient medication deleted sucessfully!")
