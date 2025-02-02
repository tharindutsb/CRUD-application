from openApi.models.intern import Interns
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException

class InternsService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client["intern_db"]["interns"]

    async def create_intern(self, interns: Interns):
        interns_dict = interns.dict()
        result = await self.db.insert_one(interns_dict)
        interns_dict["id"] = str(result.inserted_id)
        return interns_dict

    async def get_interns(self):
        interns_cursor = self.db.find()
        interns = await interns_cursor.to_list(length=100)
        return interns

    async def get_intern(self, intern_id: str):
        intern = await self.db.find_one({"intern_id": intern_id})
        if intern:
            return intern
        raise HTTPException(status_code=404, detail="Intern not found")

    async def update_intern(self, intern_id: str, intern: Interns):
        update_result = await self.db.update_one(
            {"intern_id": intern_id},
            {"$set": intern.dict()}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="intern not found")
        updated_intern = await self.db.find_one({"intern_id": intern_id})
        return updated_intern

    async def delete_intern(self, intern_id: str):
        delete_result = await self.db.delete_one({"intern_id": intern_id})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Intern not found")
        return {"message": f"intern {intern_id} deleted successfully."}
