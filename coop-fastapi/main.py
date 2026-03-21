from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine
import models

from routers import (
    students, teachers, companies, requests, notifications,
    schedule, documents, reports, auth
)

# ======================
# สร้าง Database Tables
# ======================
models.Base.metadata.create_all(bind=engine)

# ======================
# สร้างโฟลเดอร์ upload ถ้ายังไม่มี
# ======================
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "report_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

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
    allow_origins=["*"],  # หรือใส่ URL frontend ของคุณ
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Static Files (ไฟล์ที่ upload)
# ======================
# student uploaded documents
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
# report files (เช่น generated PDF ของรายงาน)
app.mount("/report_files", StaticFiles(directory=REPORT_FOLDER), name="report_files")

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