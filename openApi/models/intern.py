from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Interns(BaseModel):
    intern_id: Optional[str] = None
    name: str
    address: str
    email: str
    contact_no: str

    class Config:
        # This tells Pydantic to convert ObjectId into string for MongoDB objects
        json_encoders = {ObjectId: str}
