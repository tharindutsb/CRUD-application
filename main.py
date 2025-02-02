from fastapi import FastAPI
from openApi.routes import intern_routes

app = FastAPI()

# Include the intern routes
app.include_router(intern_routes.router)
