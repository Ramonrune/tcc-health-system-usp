from flask import Blueprint, request, g
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.appointment.dto import AppointmentCreateDTO, AppointmentUpdateDTO
from app.appointment.service import AppointmentService

appointment_service = AppointmentService()

appointment = Blueprint("appointment", __name__)

@appointment.route("/v1/appointment", methods=["GET"])
@validate()
@require_token
def list():
    return appointment_service.list(g, request)


@appointment.route("/v1/appointment/<id>", methods=["GET"])
@validate()
@require_token
def find(id):
    return appointment_service.find(g, id)


@appointment.route("/v1/appointment/<id>/entity", methods=["GET"])
@validate()
@require_token
def find_entity(id):
    return appointment_service.find_entity(g, id)


@appointment.route("/v1/appointment", methods=["POST"])
@validate()
@require_token
def register(body: AppointmentCreateDTO):
    return appointment_service.register(g, body)



@appointment.route("/v1/appointment/<id>", methods=["PUT"])
@validate()
@require_token
def update(id: str, body: AppointmentUpdateDTO):
    return appointment_service.update(g, id, body)



@appointment.route("/v1/appointment/<id>", methods=["DELETE"])
@validate()
@require_token
def delete(id:str):
    return appointment_service.delete(g, id)
