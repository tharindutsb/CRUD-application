from pydantic import BaseModel, EmailStr, field_validator

class Interns(BaseModel):
    intern_id: str
    name: str 
    address: str
    email: EmailStr
    contact_no: str  

    @field_validator('name')
    def validate_name(cls, value):
        """
        Validates the name field to ensure it contains only letters and spaces.
        """
        if not value.replace(" ", "").isalpha():
            raise ValueError('Name should only contain letters and spaces')
        return value

    @field_validator('contact_no')
    def validate_contact_no(cls, value):
        """
        Validates the contact number to ensure it starts with 0, has 10 digits, and only contains digits.
        """
        if not value.startswith('0') or len(value) != 10 or not value.isdigit():
            raise ValueError('Contact number must start with 0 and be 10 digits long')
        return value

    class Config:
        orm_mode = True
