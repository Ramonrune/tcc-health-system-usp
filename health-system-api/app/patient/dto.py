from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class PatientCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the patient")
    birth_date: date = Field(..., description="Date of birth of the patient")
    cpf: str = Field(..., description="CPF of the patient")
    email: str = Field(None, description="E-mail of the patient")
    phone: Optional[str] = Field(None, description="Phone")


class PatientUpdateDTO(BaseModel):
    name: str = Field(..., description="Name of the patient")
    phone: Optional[str] = Field(None, description="Phone")
    weight: float = Field(..., description="Weight of the patient in kilograms")
    height: float = Field(..., description="Height of the patient in meters")
    gender: str = Field(..., description="Gender of the patient (M/F)")
    birth_date: date = Field(..., description="Date of birth of the patient")
    blood_type: Optional[str] = Field(None, description="Blood type of the patient (e.g., O+, AB-)")
    smookes: int = Field(..., description="Whether the patient smookes (1/0)")
    
