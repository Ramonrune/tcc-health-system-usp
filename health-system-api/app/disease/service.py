import uuid
from sqlalchemy.exc import IntegrityError
from app.config.infra.database import db
from app.patient.model import Patient
from app.disease.dto import DiseaseCreateDTO, DiseaseUpdateDTO
from app.disease.model import Disease
from app.disease.model import PatientDisease
from app.util.response import Response
from sqlalchemy.orm import joinedload


class DiseaseService:
    
    
    def list(self, request):
        name = request.args.get("name")
        patient_id = request.args.get("patient_id", None)
        
        if patient_id == None:
            diseases = db.session.query(Disease).filter(Disease.name.like(f"%{name}%")).order_by(Disease.name.asc()).all()
            
            diseases = [disease.to_dict() for disease in diseases]
        
            return Response.ok(data=diseases, message="Diseases sucessfully found!")
        
        
        diseases = db.session.query(PatientDisease).join(Disease).filter(PatientDisease.patient_id == patient_id).order_by(PatientDisease.date_entered.desc()).all()
        
        diseases = [disease.to_dict() for disease in diseases]
        
        
        return Response.ok(data=diseases, message="Patient diseases sucessfully found!")
      
    def find(self, id: str):
        disease = (
            db.session.query(PatientDisease)
            .join(Disease)
            .filter(PatientDisease.id == id)
            .first()
        )


        return Response.ok(
            data=disease.to_dict(), message="Patient disease sucessfully found!"
        )
  

    def register(self, body: DiseaseCreateDTO):
        try:
            patient_disease = PatientDisease(
                id=str(uuid.uuid4()),
                patient_id=body.patient_id,
                disease_id=body.disease_id,
                note=body.note
            )
            db.session.add(patient_disease)
            db.session.commit()

            return Response.created(data={}, message="Patient disease sucessfully registered!")
        except IntegrityError:
            return Response.conflict(data={}, message="Patient or disease don't exist!")

  
    def update(self, id: str, body: DiseaseUpdateDTO):
        patient_disease = (
            db.session.query(PatientDisease).filter_by(id=id).first()
        )

        if patient_disease == None:
            return Response.not_found(data={}, message="Patient disease not found!")

        patient_disease.disease_id = body.disease_id
        patient_disease.note = body.note

        db.session.commit()

        return Response.ok(data={}, message="Patient disease sucessfully updated!")
    
    def delete(self, id: str):
        
        patient_disease = db.session.query(PatientDisease).filter_by(id=id).first()
        
        if patient_disease == None:
            return Response.not_found(data={}, message="Patient disease not found!")
        
        db.session.delete(patient_disease)
        
        db.session.commit()
        
        return Response.ok(data={}, message="Patient disease deleted sucessfully!")
       
       