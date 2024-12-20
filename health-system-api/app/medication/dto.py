from pydantic import BaseModel, Field


class MedicationCreateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    medication_id: str = Field(..., description="Medication id")
    note: str = Field(..., description="Notes")



class MedicationUpdateDTO(BaseModel):
    patient_id: str = Field(..., description="Patient id")
    medication_id: str = Field(..., description="Medication id")
    note: str = Field(..., description="Notes")
