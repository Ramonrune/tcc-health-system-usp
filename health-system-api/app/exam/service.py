import uuid, os
from sqlalchemy.exc import IntegrityError
from app.config.infra.database import db
from app.exam.model import Exam
from app.exam.dto import ExamCreateDTO, ExamUpdateDTO, ExamUploadDTO
from app.util.response import Response
from app.config.infra.s3 import S3


class ExamService:

    def __init__(self):
        self.s3 = S3()
        
    def register(self, g, body: ExamCreateDTO):
        exam = Exam(
            id=str(uuid.uuid4()),
            name=body.name,
            date=body.date,
            note=body.note,
            patient_id=body.patient_id,
            file_extension=body.file_extension
        )
        db.session.add(exam)
        db.session.commit()

        return Response.created(data={"id": exam.id}, message="Exam sucessfully registered!")


    def update(self, g, id: str, body: ExamUpdateDTO):
        
        exam = db.session.query(Exam).filter_by(id=id).first()
        
        if exam == None:
            return Response.not_found(data={}, message="Exam not found!")
        
        exam.name = body.name
        exam.note = body.note
        exam.file_extension = body.file_extension
        exam.date = body.date
                    
        db.session.commit()

        return Response.ok(data={}, message="Exam sucessfully updated!")
       

    def get(self, id: str):
        
        exam = db.session.query(Exam).filter_by(id=id).first()
        
        if exam:
            return Response.ok(data=exam.to_dict(), message="Exam sucessfully registered!")
        
        return Response.not_found(data={}, message="Exam not found!")
       

    def delete(self, g, id: str):
        
        exam = db.session.query(Exam).filter_by(id=id).first()
        
        if exam == None:
            return Response.not_found(data={}, message="Exam not found!")
        
        
        key = os.environ["ENVIRONMENT"] + "/" + exam.patient_id + "/" +  id +  exam.file_extension
        self.s3.delete("health-system-exam", key)
        
        db.session.delete(exam)
        
        db.session.commit()
        
        return Response.ok(data={}, message="Exam deleted sucessfully!")
       
    def get_patient_exams(self, patient_id):
        exams = db.session.query(Exam).filter_by(patient_id=patient_id).order_by(Exam.date_entered.desc()).all()
      
        exams = [exam.to_dict() for exam in exams]
                
        return Response.ok(data=exams, message="Exams sucessfully retrieved!")
    
    def exam_upload_link(self, g, id, body: ExamUploadDTO):
        key = os.environ["ENVIRONMENT"] + "/" + body.patient_id + "/" +  id + body.file_extension

        link = self.s3.create_presigned_post(
            bucket_name="health-system-exam", object_name=key
        )

        return Response.ok(
            data=link, message="Exam link sucessfully generated!"
        )

    def get_document_link(self, g, id):
        exam = db.session.query(Exam).filter_by(id=id).first()
        
        if exam == None:
            return Response.not_found(data={}, message="Patient not found!")
        
        key = os.environ["ENVIRONMENT"] + "/" + exam.patient_id + "/" +  id + exam.file_extension

        link = self.s3.generate_presigned_url(
            bucket_name="health-system-exam", object_name=key
        )

        return Response.ok(
            data={"link": link}, message="Exam link sucessfully generated!"
        )
