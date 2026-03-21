from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
import models

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# ======================
# ดึง notification ทั้งหมดสำหรับผู้ใช้ปัจจุบัน
# ======================
@router.get("/")
def get_notifications(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = current_user["role"]

    # อาจารย์ดูได้ทั้งหมด
    if role == "teacher":
        return db.query(models.Notification)\
                 .order_by(models.Notification.created_at.desc())\
                 .all()

    # นักศึกษาดูเฉพาะของตัวเอง
    elif role == "student":
        student_id = current_user["username"]
        return db.query(models.Notification)\
                 .filter(models.Notification.student_id == student_id)\
                 .order_by(models.Notification.created_at.desc())\
                 .all()

    raise HTTPException(status_code=403, detail="Invalid role")


# ======================
# ทำเครื่องหมาย notification ว่าอ่านแล้ว
# ======================
@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = db.query(models.Notification).filter(
        models.Notification.notification_id == notification_id
    ).first()

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    # นักศึกษาต้องตรวจสอบว่าเป็นของตัวเอง
    if current_user["role"] == "student" and notif.student_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="Cannot mark others' notifications")

    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif