from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from openApi.models.intern import Interns
from openApi.services.intern_service import InternsService
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from logger.TestLogger import logger  # Import logger from TestLogger.py
from fastapi import Form
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
    tags=["Interns"],
    response_description="The created intern's ID and a success message."
)
async def create_intern(
    name: str = Form(..., examples={"example": "Tharindu Sampath"}),
    address: str = Form(..., examples={"example": "123 Main St"}),
    email: str = Form(..., examples={"example": "tharindu.doe@example.com"}),
    contact_no: str = Form(..., examples={"example": "0712345678"}),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Creates a new intern and returns a success message."""
    intern = Interns(name=name, address=address, email=email, contact_no=contact_no)
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
    tags=["Interns"],
    response_description="A list of all registered interns."
)
async def get_interns(
    name: str = Query(None, description="Filter by name", examples={"example": "Tharindu"}),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return (default: 10)", examples={"example": 10}),
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
        logger.info(f"✅ Returning {len(interns[:limit])} interns")
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
    tags=["Interns"],
    response_description="The details of the requested intern."
)
async def get_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern", examples={"example": "0001"}),
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
    tags=["Interns"],
    response_description="The updated intern's details and a success message."
)
async def update_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern to update", examples={"example": "0001"}),
    intern: Interns = Body(..., examples={  # Define fields to update
        "example": {
            "name": "Updated Tharindu Sampath",
            "address": "456 Elm St",
            "email": "updated.tharindu.doe@example.com",
            "contact_no": "0712345679"
        }
    }),
    db: AsyncIOMotorClient = Depends(get_db)
):
    """Updates an intern's details by ID."""
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
    tags=["Interns"],
    response_description="A success message indicating the intern was deleted."
)
async def delete_intern(
    intern_id: str = Path(..., title="Intern ID", description="The unique ID of the intern to delete", examples={"example": "0001"}),
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
    tags=["Interns"],
    response_description="A success message indicating all interns were deleted."
)
async def delete_all_interns(db: AsyncIOMotorClient = Depends(get_db)):
    """Deletes all interns in the database."""
    try:
        intern_service = InternsService(db)
        return await intern_service.delete_all_interns()
    except Exception as e:
        logger.error(f"❌ Error deleting all interns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
