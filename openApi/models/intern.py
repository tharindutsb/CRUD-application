from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from typing import Optional

class Interns(BaseModel):
    intern_id: Optional[str] = None  # Make it optional
    name: str = Field(..., description="The name of the intern", json_schema_extra={"examples": {"example": "Tharindu Sampath"}})
    address: str = Field(..., description="The address of the intern", json_schema_extra={"examples": {"example": "123 Main St"}})
    email: EmailStr = Field(..., description="The email address of the intern", json_schema_extra={"examples": {"example": "tharindu.doe@example.com"}})
    contact_no: str = Field(..., description="The contact number of the intern", json_schema_extra={"examples": {"example": "0712345678"}})

    @field_validator("name")
    def validate_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name should only contain letters and spaces")
        return value

    @field_validator("contact_no")
    def validate_contact_no(cls, value):
        if not value.isdigit() or len(value) != 10 or not value.startswith("0"):
            raise ValueError("Contact number must start with 0 and be 10 digits long")
        return value

    model_config = ConfigDict(from_attributes=True)  # Fixes Pydantic V2 issue
