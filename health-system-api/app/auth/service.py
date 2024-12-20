import botocore
from app.config.infra.database import db
from app.config.infra.cognito import CognitoUtil
from app.auth.model import User
from app.auth.dto import AuthDTO, ForgotPasswordDTO, ConfirmForgotPasswordDTO, SignupDTO, ConfirmSignupDTO
from app.util.response import Response

class AuthService:

    def __init__(self) -> None:
        self.cognito = CognitoUtil()
        
    def authenticate(self, body: AuthDTO):
        try:
            
            user = User.query.filter_by(email=body.email).first()
            if not user:
                return Response.conflict("Account not found", {
                    "code": "AccountNotFound"
                })
            

            response = self.cognito.auth(body.email, body.password)

            data = {
                "user": user.to_dict(),
                "token": response["AuthenticationResult"]["AccessToken"]
            }

            return Response.ok(data)
        
        except botocore.exceptions.ClientError as error:

            print(error)
            import traceback
            traceback.print_exc()
            errors = {
                "UserNotFoundException": {
                    "response": lambda: Response.bad_request(
                        data={"code": "AccountNotFound"},
                        message="User not found"
                    )
                },
                "UserNotConfirmedException": {
                    "response": lambda: Response.bad_request(
                        data={"code": "UserNotConfirmedException"},
                        message="User not confirmed"
                    )
                },
                "NotAuthorizedException": {
                    "response": lambda: Response.bad_request(
                        data={"code": "NotAuthorizedException"},
                        message="Not authorized"
                    ),
                },
                "GeneralException": {
                    "response": lambda: Response.bad_request(
                        data={"code": "GeneralException"},
                        message="An error ocurred, please try again later!"
                    ),
                }
            }
            
            error_code = error.response["Error"]["Code"]
            error = errors.get(error_code, errors['GeneralException'])
            
            return error["response"]()

    
    def signup(self, body: SignupDTO):
        status, response = self.cognito.sign_up(body.email, body.password)
        
        if status == "UsernameExistsException":
            return Response.conflict("User already exists", {
                "status": "UsernameExistsException"
            })  

        user = User(id=response["UserSub"], name=body.name, email=body.email)
        db.session.add(user)
        db.session.commit()
        return Response.created(data={}, message="User created sucessfully")
    
    
    def confirm_signup(self, body: ConfirmSignupDTO):
        status, response = self.cognito.confirm_sign_up(body.email, body.code)
        if status == "CodeMismatchException":
            return Response.conflict("The code provided is wrong! Please try again.", data={
                "status": "CodeMismatchException"
            })
        
        if status == "ExpiredCodeException":
             return Response.conflict("Your code has expired!", data={
                "status": "ExpiredCodeException"
            })
                     
        return Response.ok({}, "User confirmed successfully!")

    def forgot_password(self, body: ForgotPasswordDTO):
        
        user = User.query.filter_by(email = body.email).first()
                
        if user == None:
            return Response.conflict(message="Account not found!", data={"code": "AccountNotFound"})
            
        self.cognito.forgot_password(body.email)
        
        return Response.ok({}, "Password code sent successfully!")
        

    def confirm_forgot_password(self, body: ConfirmForgotPasswordDTO):
        status, response = self.cognito.confirm_forgot_password(body.email, body.code, body.password)

        if(status != 'Success'):
            return Response.conflict(status, data={
                "status": status
            })

        return Response.ok({}, "Password changed successfully!")
    
    

    