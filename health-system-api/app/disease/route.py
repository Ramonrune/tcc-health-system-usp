from flask import Blueprint, request
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.disease.dto import DiseaseCreateDTO, DiseaseUpdateDTO
from app.disease.service import DiseaseService

disease_service = DiseaseService()

disease = Blueprint('disease', __name__)


@disease.route('/v1/disease',  methods=['GET'])
@validate()
@require_token
def list():
    return disease_service.list(request)

@disease.route('/v1/disease/<id>',  methods=['GET'])
@validate()
@require_token
def find(id):
    return disease_service.find(id)


@disease.route('/v1/disease',  methods=['POST'])
@validate()
@require_token
def register(body: DiseaseCreateDTO):
    return disease_service.register(body)

@disease.route("/v1/disease/<id>", methods=["PUT"])
@validate()
@require_token
def update(id, body: DiseaseUpdateDTO):
    return disease_service.update(id, body)



@disease.route('/v1/disease/<id>',  methods=['DELETE'])
@validate()
@require_token
def delete(id):
    return disease_service.delete(id)
    

