from flask import Blueprint, request, g
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.exam.service import ExamService
from app.exam.dto import ExamCreateDTO, ExamUpdateDTO, ExamUploadDTO

exam_service = ExamService()

exam = Blueprint('exam', __name__)
@exam.route('/v1/exam',  methods=['POST'])
@validate()
@require_token
def register(body: ExamCreateDTO):
    return exam_service.register(g, body)


@exam.route('/v1/exam/<id>',  methods=['PUT'])
@validate()
@require_token
def update(id, body: ExamUpdateDTO):
    return exam_service.update(g, id, body)

@exam.route('/v1/exam/<id>',  methods=['GET'])
@validate()
@require_token
def get(id):
    return exam_service.get(id)


@exam.route('/v1/exam',  methods=['GET'])
@require_token
def get_patient_exams():
    patient_id = request.args.get("patient_id")
    return exam_service.get_patient_exams(patient_id)


@exam.route('/v1/exam/<id>',  methods=['DELETE'])
@validate()
@require_token
def delete(id):
    return exam_service.delete(g, id)



@exam.route('/v1/exam/<id>/upload-document-link',  methods=['POST'])
@validate()
@require_token
def exam_upload_link(id, body: ExamUploadDTO):
    return exam_service.exam_upload_link(g, id, body)




@exam.route('/v1/exam/<id>/document-link',  methods=['GET'])
@require_token
def get_document_link(id):
    return exam_service.get_document_link(g, id)
