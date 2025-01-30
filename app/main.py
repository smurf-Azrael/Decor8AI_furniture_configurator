from fastapi import FastAPI
from app.routes import decor8ai
import os
from dotenv import load_dotenv

app = FastAPI(title="Decor8AI Backend")

app.include_router(decor8ai.router, prefix="/api/decor8ai")
load_dotenv()
@app.get("/")
def read_root():
    return {"message": "Welcome to Decor8AI Backend"}
