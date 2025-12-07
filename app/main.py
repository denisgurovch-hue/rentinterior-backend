from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base
from app import models

# Создать все таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RentInterior API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to RentInterior API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
