from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Fake Attendance API")

class User(BaseModel):
    id: int
    full_name: str
    email: str

class AttendanceRecord(BaseModel):
    id: int
    user_id: int
    user_name: str
    date: str
    status: str

@app.get("/", summary="API root")
async def root():
    return {"message": "Fake Attendance API is running", "status": "ok"}

@app.get("/users", response_model=List[User], summary="List users")
async def get_users():
    return [
        {"id": 1, "full_name": "Alice Johnson", "email": "alice@example.com"},
        {"id": 2, "full_name": "Bob Martinez", "email": "bob@example.com"}
    ]

@app.get("/attendance", response_model=List[AttendanceRecord], summary="List attendance records")
async def get_attendance():
    return [
        {"id": 1, "user_id": 1, "user_name": "Alice Johnson", "date": "2026-07-31", "status": "present"},
        {"id": 2, "user_id": 2, "user_name": "Bob Martinez", "date": "2026-07-31", "status": "late"}
    ]

@app.get("/status", summary="Health check")
async def status():
    return {"service": "fake_attendance_api", "status": "running"}
