import uuid, os
from sqlalchemy.exc import IntegrityError
from app.config.infra.database import db
from app.patient.model import Patient
from app.patient.model import Attend

from app.patient.dto import PatientCreateDTO, PatientUpdateDTO
from app.util.response import Response
from app.config.infra.s3 import S3


class PatientService:

    def __init__(self):
        self.s3 = S3()

    def register(self, g, body: PatientCreateDTO):
        patient = db.session.query(Patient).filter_by(cpf=body.cpf).first()
        
        if patient:
            attend = Attend(
                id=str(uuid.uuid4()),
                patient_id=patient.id,
                user_id=g.user_id,
            )
        
            db.session.add(attend)
            
            db.session.commit()
            
            return Response.created(data={}, message="Patient sucessfully registered!")

        else:
        
            patient = Patient(
                id=str(uuid.uuid4()),
                name=body.name,
                email=body.email,
                birth_date=body.birth_date,
                cpf=body.cpf,
                phone=body.phone,
            )
            db.session.add(patient)
            
            attend = Attend(
                id=str(uuid.uuid4()),
                patient_id=patient.id,
                user_id=g.user_id,
            )
            
            db.session.add(attend)
            
            db.session.commit()

            return Response.created(data={}, message="Patient sucessfully registered!")
        

    def update(self, id: str, body: PatientUpdateDTO):

        patient = db.session.query(Patient).filter_by(id=id).first()

        if patient == None:
            return Response.not_found(data={}, message="Patient not found!")

        patient.name = body.name
        patient.birth_date = body.birth_date
        patient.weight = body.weight
        patient.height = body.height
        patient.gender = body.gender
        patient.blood_type = body.blood_type
        patient.smookes = body.smookes
        patient.phone = body.phone

        db.session.commit()

        return Response.ok(data={}, message="Patient sucessfully updated!")

    def get(self, id: str):

        patient = db.session.query(Patient).filter_by(id=id).first()

        if patient:
            return Response.ok(
                data=patient.to_dict(), message="Patient sucessfully found!"
            )

        return Response.not_found(data={}, message="Patient not found!")

    def get_by_cpf(self, cpf: str):

        patient = db.session.query(Patient).filter_by(cpf=cpf).first()

        if patient:
            return Response.ok(
                data=patient.to_dict(), message="Patient sucessfully found!"
            )

        return Response.not_found(data={}, message="Patient not found!")

    def delete(self, g, id: str):

        attend = db.session.query(Attend).filter_by(user_id=g.user_id, patient_id=id).first()

        if attend == None:
            return Response.not_found(data={}, message="Patient attend not found!")

        db.session.delete(attend)

        db.session.commit()

        return Response.ok(data={}, message="Patient attend deleted sucessfully!")

    def profile_picture_upload_link(self, g, id):
        key = os.environ["ENVIRONMENT"] + "/" + id + ".jpg"

        link = self.s3.create_presigned_post(
            bucket_name="health-system-profile", object_name=key
        )

        return Response.ok(
            data=link, message="Profile picture link sucessfully generated!"
        )

    def profile_picture_link(self, g, id):
        key = os.environ["ENVIRONMENT"] + "/" + id + ".jpg"

        link = self.s3.generate_presigned_url(
            bucket_name="health-system-profile", object_name=key
        )

        return Response.ok(
            data={"link": link}, message="Profile picture link sucessfully generated!"
        )

    def find_doctor_patients(self, g):
        user_id = g.user_id

        patients = (
            db.session.query(Patient)
            .join(Attend)
            .filter(Attend.user_id == user_id)
            .order_by(Patient.name.asc())
            .all()
        )

        patients = [patient.to_dict() for patient in patients]

        return Response.ok(data=patients, message="Patients sucessfully found!")
