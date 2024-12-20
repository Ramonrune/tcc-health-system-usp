from flask import Blueprint, request
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.medication.dto import MedicationCreateDTO, MedicationUpdateDTO
from app.medication.service import MedicationService

medication_service = MedicationService()

medication = Blueprint("Medication", __name__)


@medication.route("/v1/medication", methods=["GET"])
@validate()
@require_token
def list():
    return medication_service.list(request)


@medication.route("/v1/medication/<id>", methods=["GET"])
@validate()
@require_token
def find(id):
    return medication_service.find(id)

@medication.route("/v1/medication", methods=["POST"])
@validate()
@require_token
def register(body: MedicationCreateDTO):
    return medication_service.register(body)


@medication.route("/v1/medication/<id>", methods=["PUT"])
@validate()
@require_token
def update(id, body: MedicationUpdateDTO):
    return medication_service.update(id, body)

@medication.route("/v1/medication/<id>", methods=["DELETE"])
@validate()
@require_token
def delete(id):
    return medication_service.delete(id)
