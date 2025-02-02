from pydantic import BaseModel
from bson import ObjectId

class Interns(BaseModel):
    intern_id: str
    name: str
    address: str
    email: str
    contact_no: str

    class Config:
        # This tells Pydantic to convert ObjectId into string for MongoDB objects
        json_encoders = {ObjectId: str}
