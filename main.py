from fastapi import FastAPI, HTTPException
from openApi.routes.intern_routes import router as intern_router
import logging


app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    app.include_router(intern_router)
except Exception as e:
    logger.error(f"Failed to include intern routes: {e}")

@app.get("/")
def read_root():
    try:
        return {"message": "Welcome to the Intern API"}
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
