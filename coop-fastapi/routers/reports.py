from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
import models

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# Schema สำหรับรับข้อมูล
class ReportCreate(BaseModel):
    student_id: int
    teacher_id: int
    title: str
    description: str


# ดูรายงานทั้งหมด
@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    return db.query(models.Report).all()


# ดูรายงานของ student
@router.get("/student/{student_id}")
def get_student_reports(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(
        models.Report.student_id == student_id
    ).all()


# เพิ่มรายงาน
@router.post("/")
def create_report(data: ReportCreate, db: Session = Depends(get_db)):

    new_report = models.Report(
        student_id=data.student_id,
        teacher_id=data.teacher_id,
        title=data.title,
        description=data.description,
        submitted_at=datetime.now()
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "report created",
        "data": new_report
    }