from fastapi import APIRouter, Depends, HTTPException
from openApi.models.intern import Interns
from openApi.services.intern_service import InternsService
from motor.motor_asyncio import AsyncIOMotorClient
import logging

router = APIRouter()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency to get the database client
def get_db():
    try:
        return AsyncIOMotorClient("mongodb://localhost:27017")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@router.post("/interns/")
async def create_intern(intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.create_intern(intern)
    except Exception as e:
        logger.error(f"Error creating intern: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/interns/")
async def get_interns(db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.get_interns()
    except Exception as e:
        logger.error(f"Error fetching interns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/interns/{intern_id}")
async def get_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.get_intern(intern_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error retrieving intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/interns/{intern_id}")
async def update_intern(intern_id: str, intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.update_intern(intern_id, intern)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error updating intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/interns/{intern_id}")
async def delete_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.delete_intern(intern_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error deleting intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/interns/")
async def delete_all_interns(db: AsyncIOMotorClient = Depends(get_db)):
    try:
        intern_service = InternsService(db)
        return await intern_service.delete_all_interns()
    except Exception as e:
        logger.error(f"Error deleting all interns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
