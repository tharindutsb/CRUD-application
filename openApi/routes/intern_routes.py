from fastapi import APIRouter, Depends
from openApi.models.intern import Interns
from openApi.services.intern_service import InternsService
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# Dependency to get the database client
def get_db():
    return AsyncIOMotorClient("mongodb://localhost:27017")

# API route to create an intern
@router.post("/interns/")
async def create_intern(intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
    intern_service = InternsService(db)
    return await intern_service.create_intern(intern)

# API route to retrieve all interns
@router.get("/interns/")
async def get_interns(db: AsyncIOMotorClient = Depends(get_db)):
    intern_service = InternsService(db)
    return await intern_service.get_interns()

# API route to retrieve a specific intern by intern_id
@router.get("/interns/{intern_id}")
async def get_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    intern_service = InternsService(db)
    return await intern_service.get_intern(intern_id)

# API route to update an intern's details
@router.put("/interns/{intern_id}")
async def update_intern(intern_id: str, intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
    intern_service = InternsService(db)
    return await intern_service.update_intern(intern_id, intern)

# API route to remove an intern
@router.delete("/interns/{intern_id}")
async def delete_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    intern_service = InternsService(db)
    return await intern_service.delete_intern(intern_id)
