from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

from routers import students, teachers, companies, requests, notifications, schedule, documents, reports, auth


# ======================
# Create Database Tables
# ======================
models.Base.metadata.create_all(bind=engine)


# ======================
# FastAPI App
# ======================
app = FastAPI(
    title="Coop System API",
    description="API สำหรับระบบบริหารจัดการสหกิจศึกษา",
    version="1.0.0"
)


# ======================
# CORS (สำหรับ Frontend)
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================
# Routers
# ======================
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(companies.router)
app.include_router(requests.router)
app.include_router(documents.router)
app.include_router(reports.router)
app.include_router(notifications.router)
app.include_router(schedule.router)


# ======================
# Root API
# ======================
@app.get("/")
def root():
    return {
        "message": "Welcome to Coop System API",
        "docs": "/docs"
    }