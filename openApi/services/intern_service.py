from openApi.models.intern import Interns
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException

class InternsService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client["intern_db"]["interns"]
        self.counter_db = db_client["intern_db"]["counters"]  # For managing intern_id counter

    async def get_next_intern_id():
        # Find and update the counter for 'intern_id'
        counter = await self.counter_db.find_one_and_update(
            {"_id": "intern_id"},
            {"$inc": {"seq": 1}},  # Increment the counter by 1
            upsert=True,  # Create the counter if it doesn't exist
            return_document=True  # Return the updated counter
        )
        # Return the next ID, formatted to four digits
        return str(counter["seq"]).zfill(4)

    async def create_intern(self, intern: Interns):
        intern_dict = intern.dict(exclude_unset=True)

        # Generate the next intern_id
        intern_id = await self.get_next_intern_id()

        # Assign the generated intern_id to the intern object
        intern_dict["intern_id"] = intern_id
        
        # Insert the intern into the MongoDB collection
        result = await self.db.insert_one(intern_dict)
        intern_dict["id"] = str(result.inserted_id)  # Add the MongoDB _id to the response
        return intern_dict

    async def get_interns(self):
        interns_cursor = self.db.find()
        interns = await interns_cursor.to_list(length=100)
        for intern in interns:
            intern["_id"] = str(intern["_id"])
        return interns

    async def get_intern(self, intern_id: str):
        intern = await self.db.find_one({"intern_id": intern_id})
        if intern:
            intern["_id"] = str(intern["_id"])
            return intern
        raise HTTPException(status_code=404, detail="Intern not found")

    async def update_intern(self, intern_id: str, intern: Interns):
        update_result = await self.db.update_one(
            {"intern_id": intern_id},
            {"$set": intern.dict(exclude_unset=True)}  # Update only the fields provided
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Intern not found")
        updated_intern = await self.db.find_one({"intern_id": intern_id})
        if updated_intern:
            updated_intern["_id"] = str(updated_intern["_id"])
        return updated_intern

    async def delete_intern(self, intern_id: str):
        delete_result = await self.db.delete_one({"intern_id": intern_id})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Intern not found")
        return {"message": f"Intern {intern_id} deleted successfully."}
