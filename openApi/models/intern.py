from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class Interns(BaseModel):
    intern_id: Optional[str] = None  # Make it optional
    name: str
    address: str
    email: EmailStr
    contact_no: str

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

    class Config:
        from_attributes = True  # Fixes Pydantic V2 issue
