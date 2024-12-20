from pydantic import BaseModel, Field


class DiseaseCreateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    disease_id: str = Field(..., description="Disease id")
    note: str = Field(..., description="Note")


class DiseaseUpdateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    disease_id: str = Field(..., description="Disease id")
    note: str = Field(..., description="Note")
