# from fastapi import APIRouter, Depends, HTTPException
# from openApi.models.intern import Interns
# from openApi.services.intern_service import InternsService
# from motor.motor_asyncio import AsyncIOMotorClient
# import logging

# router = APIRouter()

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Dependency to get the database client
# def get_db():
#     """Returns the MongoDB client connection."""
#     try:
#         return AsyncIOMotorClient("mongodb://localhost:27017")
#     except Exception as e:
#         logger.error(f"❌ Database connection error: {e}")
#         raise HTTPException(status_code=500, detail="Database connection failed")

# # ✅ FIX 1: Define API response model for correct Swagger validation
# @router.post("/interns/", response_model=dict, summary="Create a new intern", tags=["Interns"])
# async def create_intern(intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Creates a new intern and returns a success message.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.create_intern(intern)
#     except Exception as e:
#         logger.error(f"❌ Error creating intern: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/interns/", response_model=list, summary="Get all interns", tags=["Interns"])
# async def get_interns(db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Returns a list of all registered interns.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.get_interns()
#     except Exception as e:
#         logger.error(f"❌ Error fetching interns: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/interns/{intern_id}", response_model=dict, summary="Get an intern by ID", tags=["Interns"])
# async def get_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Returns details of a specific intern by ID.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.get_intern(intern_id)
#     except HTTPException as http_error:
#         raise http_error
#     except Exception as e:
#         logger.error(f"❌ Error retrieving intern with ID {intern_id}: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# # ✅ FIX 2: Ensure correct response model & error handling for updates
# @router.put("/interns/{intern_id}", response_model=dict, summary="Update an intern", tags=["Interns"])
# async def update_intern(intern_id: str, intern: Interns, db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Updates an intern's details.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.update_intern(intern_id, intern)
#     except HTTPException as http_error:
#         raise http_error
#     except Exception as e:
#         logger.error(f"❌ Error updating intern with ID {intern_id}: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.delete("/interns/{intern_id}", response_model=dict, summary="Delete an intern by ID", tags=["Interns"])
# async def delete_intern(intern_id: str, db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Deletes an intern by ID.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.delete_intern(intern_id)
#     except HTTPException as http_error:
#         raise http_error
#     except Exception as e:
#         logger.error(f"❌ Error deleting intern with ID {intern_id}: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# # ✅ FIX 3: Add method to delete all interns
# @router.delete("/interns/", response_model=dict, summary="Delete all interns", tags=["Interns"])
# async def delete_all_interns(db: AsyncIOMotorClient = Depends(get_db)):
#     """
#     ✅ Deletes all interns in the database.
#     """
#     try:
#         intern_service = InternsService(db)
#         return await intern_service.delete_all_interns()
#     except Exception as e:
#         logger.error(f"❌ Error deleting all interns: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


from fastapi import APIRouter, Depends, HTTPException, Query, Path
from openApi.models.intern import Interns
from openApi.services.intern_service import InternsService
from motor.motor_asyncio import AsyncIOMotorClient
import logging

router = APIRouter()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Database Dependency
def get_db():
    """Returns the MongoDB client connection."""
    try:
        return AsyncIOMotorClient("mongodb://localhost:27017")
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# ✅ Create an intern with request body validation
@router.post(
    "/interns/",
    response_model=dict,
    summary="Create a new intern",
    description="Adds a new intern to the database.",
    tags=["Interns"]
)
async def create_intern(
    intern: Interns,
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Creates a new intern and returns a success message."""
    try:
        intern_service = InternsService(db)
        return await intern_service.create_intern(intern)
    except Exception as e:
        logger.error(f"❌ Error creating intern: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Get all interns with optional filters
@router.get(
    "/interns/",
    response_model=list,
    summary="Get all interns",
    description="Returns a list of all registered interns. You can filter results.",
    tags=["Interns"]
)
async def get_interns(
    name: str = Query(None, description="Filter by name"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return (default: 10)"),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Fetch all interns with optional name filtering."""
    try:
        intern_service = InternsService(db)
        interns = await intern_service.get_interns()

        # Apply optional filtering by name
        if name:
            interns = [intern for intern in interns if name.lower() in intern["name"].lower()]

        # Limit results
        return interns[:limit]
    except Exception as e:
        logger.error(f"❌ Error fetching interns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Get an intern by ID with validation
@router.get(
    "/interns/{intern_id}",
    response_model=dict,
    summary="Get an intern by ID",
    description="Retrieves details of a specific intern using their intern ID.",
    tags=["Interns"]
)
async def get_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern"),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Returns details of a specific intern by ID."""
    try:
        intern_service = InternsService(db)
        return await intern_service.get_intern(intern_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"❌ Error retrieving intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Update an intern with validation
@router.put(
    "/interns/{intern_id}",
    response_model=dict,
    summary="Update an intern",
    description="Updates an intern's details by ID.",
    tags=["Interns"]
)
async def update_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern to update"),
    intern: Interns = Depends(),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Updates an intern's details."""
    try:
        intern_service = InternsService(db)
        return await intern_service.update_intern(intern_id, intern)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"❌ Error updating intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Delete an intern by ID
@router.delete(
    "/interns/{intern_id}",
    response_model=dict,
    summary="Delete an intern by ID",
    description="Deletes an intern from the database using their ID.",
    tags=["Interns"]
)
async def delete_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern to delete"),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Deletes an intern by ID."""
    try:
        intern_service = InternsService(db)
        return await intern_service.delete_intern(intern_id)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"❌ Error deleting intern with ID {intern_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Delete all interns
@router.delete(
    "/interns/",
    response_model=dict,
    summary="Delete all interns",
    description="⚠️ Deletes all interns from the database. **Use with caution!**",
    tags=["Interns"]
)
async def delete_all_interns(db: AsyncIOMotorClient = Depends(get_db)):
    """Deletes all interns in the database."""
    try:
        intern_service = InternsService(db)
        return await intern_service.delete_all_interns()
    except Exception as e:
        logger.error(f"❌ Error deleting all interns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
