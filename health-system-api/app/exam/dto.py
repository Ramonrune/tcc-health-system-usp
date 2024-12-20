from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class ExamCreateDTO(BaseModel):
    name: str = Field(..., description="Name")
    note: str = Field(..., description="Name of the patient")
    date:  str = Field(..., description="Date of exam")
    patient_id: str = Field(..., description="Patient id")
    file_extension: str =  Field(..., description="File extension")
    
   

class ExamUpdateDTO(BaseModel):
    name: str = Field(..., description="Name")
    note: str = Field(..., description="Name of the patient")
    date:  str = Field(..., description="Date of exam")
    patient_id: str = Field(..., description="Patient id")
    file_extension: str =  Field(..., description="File extension")


class ExamUploadDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    file_extension: str = Field(..., description="File extension support (.png, .jpg, .jpeg, .pdf, .zip)")
    