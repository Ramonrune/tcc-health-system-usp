import os
from flask import Flask, request
from app.config.infra.cors import Cors
from app.config.infra.database import db, init_db
from app.auth.route import auth
from app.patient.route import patient
from app.exam.route import exam
from app.disease.route import disease
from app.medication.route import medication
from app.appointment.route import appointment
from app.dashboard.route import dashboard

cors = Cors()
app = Flask(__name__)

init_db(app)


with app.app_context():
    db.create_all()

app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(exam)
app.register_blueprint(disease)
app.register_blueprint(medication)
app.register_blueprint(appointment)
app.register_blueprint(dashboard)

@app.after_request
def after_request(response):
    response = cors.add_cors_headers(request, response)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)