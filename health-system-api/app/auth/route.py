from flask import Blueprint
from flask_pydantic import validate
from app.auth.service import AuthService
from app.auth.dto import AuthDTO, SignupDTO, ForgotPasswordDTO, ConfirmForgotPasswordDTO, ConfirmSignupDTO

auth_service = AuthService()

auth = Blueprint('auth', __name__)
@auth.route('/v1/auth',  methods=['POST'])
@validate()
def authenticate(body: AuthDTO):
    return auth_service.authenticate(body)


@auth.route('/v1/auth/signup',  methods=['POST'])
@validate()
def signup(body: SignupDTO):
    return auth_service.signup(body)


@auth.route('/v1/auth/signup/confirm',  methods=['POST'])
@validate()
def confirm_signup(body: ConfirmSignupDTO):
    return auth_service.confirm_signup(body)

@auth.route('/v1/auth/forgot-password',  methods=['POST'])
@validate()
def forgot_password(body: ForgotPasswordDTO):
    return auth_service.forgot_password(body)


@auth.route('/v1/auth/forgot-password/confirm',  methods=['POST'])
@validate()
def confirm_forgot_password(body: ConfirmForgotPasswordDTO):
    return auth_service.confirm_forgot_password(body)