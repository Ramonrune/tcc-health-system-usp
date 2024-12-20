from pydantic import BaseModel, Field

class AuthDTO(BaseModel):
    email: str = Field(..., description="E-mail")
    password: str = Field(..., description="Password")



class ForgotPasswordDTO(BaseModel):
    email: str = Field(..., description="E-mail")



class ConfirmForgotPasswordDTO(BaseModel):
    email: str = Field(..., description="E-mail")
    password: str = Field(..., description="Password")
    code: str = Field(..., description="Activation code")


class SignupDTO(BaseModel):
    name: str = Field(..., description="Name")
    email: str = Field(..., description="E-mail")
    password: str = Field(..., description="Password")
    
    
class ConfirmSignupDTO(BaseModel):
    email: str = Field(..., description="E-mail")
    code: str = Field(..., description="Activation code")
