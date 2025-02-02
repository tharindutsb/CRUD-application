from openApi.models.intern import Interns
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException
from logger.log_config import logger  # Import logger from log_config.py

class InternsService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client["intern_db"]["interns"]
        self.counter_db = db_client["intern_db"]["counters"]

    async def get_next_intern_id(self):
        try:
            counter = await self.counter_db.find_one_and_update(
                {"_id": "intern_id"},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=True
            )
            if not counter:
                raise HTTPException(status_code=500, detail="Failed to generate intern ID")
            return str(counter["seq"]).zfill(4)
        except Exception as e:
            logger.error(f"❌ Error generating intern ID: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create_intern(self, intern: Interns):
        try:
            intern_dict = intern.model_dump(exclude_unset=True)

            # Generate intern_id
            intern_id = await self.get_next_intern_id()
            intern_dict["intern_id"] = intern_id  # Assign auto-generated ID

            # Insert into MongoDB
            result = await self.db.insert_one(intern_dict)

            # Convert MongoDB `_id` (ObjectId) to a string
            intern_dict["_id"] = str(result.inserted_id)

            logger.info(f"✅ Created new intern: {intern_id} - {intern_dict['name']}")

            # Return a structured JSON response
            return {
                "message": "User created successfully",
                "intern_id": intern_id,
                "name": intern_dict["name"]
            }
        except Exception as e:
            logger.error(f"❌ Error creating intern: {e}")
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    async def get_interns(self):
        try:
            interns_cursor = self.db.find()
            interns = await interns_cursor.to_list(length=100)

            # Convert `_id` (ObjectId) to string for each intern
            for intern in interns:
                intern["_id"] = str(intern["_id"])

            logger.info(f"✅ Fetched {len(interns)} interns")
            return interns
        except Exception as e:
            logger.error(f"❌ Error retrieving interns: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_intern(self, intern_id: str):
        try:
            intern = await self.db.find_one({"intern_id": intern_id})
            if intern:
                intern["_id"] = str(intern["_id"])  # Convert `_id`
                logger.info(f"✅ Fetched intern with intern_id: {intern_id}")
                return intern
            else:
                logger.warning(f"⚠️ Intern with intern_id {intern_id} not found")
                raise HTTPException(status_code=404, detail="Intern not found")
        except Exception as e:
            logger.error(f"❌ Error retrieving intern {intern_id}: {e}")
            raise HTTPException(status_code=404, detail="Intern not found")
    
    async def update_intern(self, intern_id: str, intern: Interns):
        try:
            update_data = intern.model_dump(exclude_unset=True)
            update_result = await self.db.update_one(
                {"intern_id": intern_id},
                {"$set": update_data}
            )

            if update_result.modified_count == 0:
                logger.warning(f"⚠️ No changes made for intern_id {intern_id}")
                raise HTTPException(status_code=404, detail="Intern not found")

            updated_intern = await self.db.find_one({"intern_id": intern_id})
            updated_intern["_id"] = str(updated_intern["_id"])  # Convert `_id`
            logger.info(f"✅ Updated intern with intern_id {intern_id}")

            return {
                "message": "User updated successfully",
                "intern_id": intern_id,
                "name": updated_intern["name"]
            }
        except Exception as e:
            logger.error(f"❌ Error updating intern {intern_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def delete_intern(self, intern_id: str):
        try:
            delete_result = await self.db.delete_one({"intern_id": intern_id})
            if (delete_result.deleted_count == 0):
                logger.warning(f"⚠️ Intern {intern_id} not found for deletion")
                raise HTTPException(status_code=404, detail="Intern not found")

            logger.info(f"✅ Deleted intern {intern_id}")
            return {"message": f"Intern {intern_id} deleted successfully."}
        except Exception as e:
            logger.error(f"❌ Error deleting intern {intern_id}: {e}")
            raise HTTPException(status_code=404, detail="Intern not found")

    async def delete_all_interns(self):
        try:
            delete_result = await self.db.delete_many({})
            logger.info(f"✅ Deleted all interns, count: {delete_result.deleted_count}")
            return {"message": f"All interns deleted successfully, count: {delete_result.deleted_count}"}
        except Exception as e:
            logger.error(f"❌ Error deleting all interns: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
