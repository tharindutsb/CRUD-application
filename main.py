from fastapi import FastAPI
from openApi.routes.intern_routes import router as intern_router

app = FastAPI()

# Include the intern routes
app.include_router(intern_router)
