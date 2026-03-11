from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# ดูรายงานทั้งหมด
@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    return db.query(models.Report).all()

# ดูรายงานตาม student
@router.get("/student/{student_id}")
def get_student_reports(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.student_id == student_id).all()

# เพิ่มรายงาน
@router.post("/")
def create_report(student_id: int, title: str, description: str, db: Session = Depends(get_db)):
    new_report = models.Report(
        student_id=student_id,
        title=title,
        description=description
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report