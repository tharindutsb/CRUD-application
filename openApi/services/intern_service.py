from openApi.models.intern import Interns
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException
from logger.log_config import logger  # Importing logger from the logger module

class InternsService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client["intern_db"]["interns"]
        self.counter_db = db_client["intern_db"]["counters"]  # For managing intern_id counter

    async def get_next_intern_id(self):
        """
        Retrieves the next intern_id by incrementing the sequence in the 'counters' collection.
        It uses a counter document with '_id' as 'intern_id' to keep track of the intern_id value.
        """
        try:
            counter = await self.counter_db.find_one_and_update(
                {"_id": "intern_id"},
                {"$inc": {"seq": 1}},  # Increment the counter by 1
                upsert=True,  # If the counter document doesn't exist, create it
                return_document=True  # Return the updated counter document
            )
            # Return the next intern_id formatted to 4 digits
            intern_id = str(counter["seq"]).zfill(4)
            return intern_id
        except Exception as e:
            logger.error(f"Error getting next intern_id: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create_intern(self, intern: Interns):
        """
        Creates a new intern and generates a unique intern_id using the get_next_intern_id method.
        Inserts the new intern into the MongoDB collection.
        """
        try:
            # Convert the Pydantic model to a dictionary, excluding unset fields
            intern_dict = intern.dict(exclude_unset=True)

            # Generate the next intern_id
            intern_id = await self.get_next_intern_id()
            intern_dict["intern_id"] = intern_id

            # Insert the intern into the MongoDB collection
            result = await self.db.insert_one(intern_dict)

            # Add the MongoDB _id to the response and log the created intern
            intern_dict["id"] = str(result.inserted_id)
            logger.info(f"Created new intern: {intern_id} - {intern_dict['name']}")
            return intern_dict

        except Exception as e:
            logger.error(f"Error creating intern: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_interns(self):
        """
        Retrieves all interns from the database.
        """
        try:
            interns_cursor = self.db.find()
            interns = await interns_cursor.to_list(length=100)

            # Convert MongoDB _id to string for each intern
            for intern in interns:
                intern["id"] = str(intern["_id"])  # Convert ObjectId to string
                del intern["_id"]  # Remove _id to prevent it from being returned in the response

            logger.info(f"Fetched {len(interns)} interns")
            return interns

        except Exception as e:
            logger.error(f"Error retrieving interns: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_intern(self, intern_id: str):
        """
        Retrieves an intern by their unique intern_id.
        """
        try:
            intern = await self.db.find_one({"intern_id": intern_id})
            if intern:
                intern["id"] = str(intern["_id"])  # Convert ObjectId to string
                del intern["_id"]  # Remove _id from the response
                logger.info(f"Fetched intern with intern_id: {intern_id}")
                return intern
            else:
                logger.warning(f"Intern with intern_id {intern_id} not found")
                raise HTTPException(status_code=404, detail="Intern not found")
        except Exception as e:
            logger.error(f"Error retrieving intern with intern_id {intern_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update_intern(self, intern_id: str, intern: Interns):
        """
        Updates the details of an existing intern using their intern_id.
        """
        try:
            update_result = await self.db.update_one(
                {"intern_id": intern_id},
                {"$set": intern.dict(exclude_unset=True)}  # Update only the fields provided
            )

            if update_result.modified_count == 0:
                logger.warning(f"No changes made for intern_id {intern_id}")
                raise HTTPException(status_code=404, detail="Intern not found")

            updated_intern = await self.db.find_one({"intern_id": intern_id})
            updated_intern["id"] = str(updated_intern["_id"])  # Convert ObjectId to string
            del updated_intern["_id"]
            logger.info(f"Updated intern with intern_id {intern_id}")
            return updated_intern

        except Exception as e:
            logger.error(f"Error updating intern with intern_id {intern_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def delete_intern(self, intern_id: str):
        """
        Deletes an intern from the database using their intern_id.
        """
        try:
            delete_result = await self.db.delete_one({"intern_id": intern_id})

            if delete_result.deleted_count == 0:
                logger.warning(f"Intern with intern_id {intern_id} not found for deletion")
                raise HTTPException(status_code=404, detail="Intern not found")

            logger.info(f"Deleted intern with intern_id {intern_id}")
            return {"message": f"Intern {intern_id} deleted successfully."}

        except Exception as e:
            logger.error(f"Error deleting intern with intern_id {intern_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
