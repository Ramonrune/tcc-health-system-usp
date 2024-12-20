from flask import Blueprint, request, g
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.patient.service import PatientService
from app.patient.dto import PatientCreateDTO, PatientUpdateDTO

patient_service = PatientService()

patient = Blueprint('patient', __name__)
@patient.route('/v1/patient',  methods=['POST'])
@validate()
@require_token
def register(body: PatientCreateDTO):
    return patient_service.register(g, body)


@patient.route('/v1/patient/<id>',  methods=['PUT'])
@validate()
@require_token
def update(id, body: PatientUpdateDTO):
    return patient_service.update(id, body)

@patient.route('/v1/patient/<id>',  methods=['GET'])
@validate()
@require_token
def get(id):
    return patient_service.get(id)


@patient.route('/v1/patient',  methods=['GET'])
@validate()
@require_token
def get_by_cpf():
    cpf = request.args.get("cpf")
    return patient_service.get_by_cpf(cpf)

@patient.route('/v1/patient/<id>',  methods=['DELETE'])
@validate()
@require_token
def delete(id):
    return patient_service.delete(g, id)


@patient.route('/v1/patient/<id>/profile-picture/upload-link',  methods=['POST'])
@require_token
def profile_picture_upload_link(id):
    return patient_service.profile_picture_upload_link(g, id)




@patient.route('/v1/patient/<id>/profile-picture-link',  methods=['GET'])
@require_token
def profile_picture_link(id):
    return patient_service.profile_picture_link(g, id)




@patient.route('/v1/doctor/patient',  methods=['GET'])
@validate()
@require_token
def find_doctor_patients():
    return patient_service.find_doctor_patients(g)