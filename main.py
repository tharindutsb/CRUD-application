from fastapi import FastAPI
from openApi.routes import student_routes

app = FastAPI()

# Include the student routes
app.include_router(student_routes.router)
