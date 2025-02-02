from fastapi import FastAPI
from openApi.routes.intern_routes import router as intern_router

app = FastAPI()

# Include intern API routes
app.include_router(intern_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Intern API"}
