from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.db import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="RentInterior API",
    description="API for RentInterior project management",
    version="1.0.0"
)


@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Welcome to RentInterior API", "version": "1.0.0"}
    )


@app.get("/health")
async def health():
    return JSONResponse(
        content={"status": "healthy", "service": "RentInterior API"}
    )

