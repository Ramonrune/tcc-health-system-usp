from pydantic import BaseModel, Field


class AppointmentCreateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    annotation: str = Field(..., description="Annotation")


class AppointmentUpdateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    annotation: str = Field(..., description="Annotation")
    
