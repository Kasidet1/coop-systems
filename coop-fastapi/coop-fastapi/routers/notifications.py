from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/")
def get_notifications(
    role: str = Query(...),
    student_id: str = Query(None),
    db: Session = Depends(get_db)
):

    # อาจารย์ดูได้ทั้งหมด
    if role == "teacher":
        return db.query(models.Notification).all()

    # นักศึกษาดูเฉพาะของตัวเอง
    elif role == "student":
        return db.query(models.Notification).filter(
            models.Notification.student_id == student_id
        ).all()

    return {"error": "invalid role"}