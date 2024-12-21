import uuid
from sqlalchemy.exc import IntegrityError
from app.config.infra.database import db
from app.config.infra.text_analytic import TextAnalytic

from app.patient.model import Patient
from app.appointment.dto import AppointmentCreateDTO, AppointmentUpdateDTO
from app.appointment.model import Appointment, AppointmentEntity
from app.util.response import Response
from sqlalchemy.orm import joinedload


class AppointmentService:

    def __init__(self):
        self.text_analytic = TextAnalytic()

    def list(self, g, request):
        user_id = g.user_id
        patient_id = request.args.get("patient_id", None)

        appointments = []
        if patient_id:
            appointments = (
                db.session.query(Appointment)
                .filter_by(patient_id=patient_id, user_id=user_id)
                .order_by(Appointment.date_entered.desc())
                .all()
            )

            appointments = [appointment.to_dict() for appointment in appointments]
        else:
            start_date = request.args.get("start_date", None)
            end_date = request.args.get("end_date", None)

            apts = (
                db.session.query(
                    Patient.id,
                    Patient.cpf,
                    Patient.name,
                    Patient.birth_date,
                    Appointment.date_entered,
                )
                .join(Appointment)
                .filter_by(user_id=user_id)
                .filter(
                    Appointment.date_entered.between(
                        start_date + " 00:00:00", end_date + " 23:59:59"
                    )
                )
                .order_by(Appointment.date_entered.desc())
                .all()
            )

            for appointment in apts:
                appointments.append(
                    {
                        "id": appointment.id,
                        "cpf": appointment.cpf,
                        "name": appointment.name,
                        "birth_date": appointment.birth_date.strftime("%Y-%m-%d"),
                        "date_entered": appointment.date_entered.strftime(
                            "%d/%m/%Y %H:%M:%S"
                        ),
                    }
                )

        return Response.ok(data=appointments, message="Appointments sucessfully found!")

    def find(self, g, id):
        user_id = g.user_id

        appointment = (
            db.session.query(Appointment)
            .filter_by(appointment_id=id, user_id=user_id)
            .first()
        )

        appointment = appointment.to_dict()

        return Response.ok(
            data=appointment, message="Patient appointment sucessfully found!"
        )

    def find_entity(self, g, id):
        entities = (
            db.session.query(AppointmentEntity).filter_by(appointment_id=id).all()
        )

        entities = [entity.to_dict() for entity in entities]

        return Response.ok(
            data=entities, message="Patient appointment entities sucessfully found!"
        )

    def register(self, g, body: AppointmentCreateDTO):
        try:
            user_id = g.user_id

            appointment = Appointment(
                appointment_id=str(uuid.uuid4()),
                user_id=user_id,
                patient_id=body.patient_id,
                annotation=body.annotation.replace("\n", " ").replace("\r", ""),
            )
            db.session.add(appointment)
            db.session.commit()

            self.__analyze(db, appointment.appointment_id, body.annotation)

            return Response.created(
                data={}, message="Patient appointment sucessfully registered!"
            )

        except IntegrityError:
            return Response.conflict(data={}, message="Patient or appointment error!")

    def update(self, g, id: str, body: AppointmentUpdateDTO):

        user_id = g.user_id

        appointment = (
            db.session.query(Appointment)
            .filter_by(appointment_id=id, user_id=user_id, patient_id=body.patient_id)
            .first()
        )

        if appointment == None:
            return Response.not_found(data={}, message="Patient appointment not found!")

        appointment.annotation = body.annotation

        AppointmentEntity.query.filter(AppointmentEntity.appointment_id == id).delete(
            synchronize_session=False
        )

        self.__analyze(db, id, body.annotation)
        
        db.session.commit()

        return Response.ok(data={}, message="Patient appointment updated sucessfully!")

    def __analyze(self, db, id, text):
        docs = self.text_analytic.analyze(text.replace("\n", " ").replace("\r", ""))
        for idx, doc in enumerate(docs):
            for entity in doc.entities:
                entity_id = str(uuid.uuid4())
                entity = AppointmentEntity(
                    id=entity_id,
                    appointment_id=id,
                    entity_text=entity.text,
                    category=entity.category,
                    sub_category=entity.subcategory,
                    offset=entity.offset,
                    confidence=entity.confidence_score,
                )

                db.session.add(entity)

    def delete(self, g, id: str):

        user_id = g.user_id

        appointment = (
            db.session.query(Appointment)
            .filter_by(appointment_id=id, user_id=user_id)
            .first()
        )

        if appointment == None:
            return Response.not_found(data={}, message="Patient appointment not found!")

        AppointmentEntity.query.filter(AppointmentEntity.appointment_id == id).delete(
            synchronize_session=False
        )

        db.session.delete(appointment)

        db.session.commit()

        return Response.ok(data={}, message="Patient appointment deleted sucessfully!")
