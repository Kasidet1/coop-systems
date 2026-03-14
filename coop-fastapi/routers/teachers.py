from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from datetime import datetime

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

# ======================
# ดูอาจารย์ทั้งหมด
# ======================
@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()


# ======================
# เพิ่มอาจารย์
# ======================
@router.post("/")
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):

    new_teacher = models.Teacher(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        email=teacher.email,
        phone=teacher.phone,
        faculty=teacher.faculty,
        created_at=datetime.now()
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher


# ======================
# แก้ไขข้อมูลอาจารย์ (แก้ได้เฉพาะตัวเอง)
# ======================
@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    teacher: schemas.TeacherCreate,
    login_teacher_id: int = Query(...),
    db: Session = Depends(get_db)
):

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.teacher_id == teacher_id
    ).first()

    if not db_teacher:
        return {"error": "Teacher not found"}

    # เช็คว่าเป็นเจ้าของข้อมูลหรือไม่
    if teacher_id != login_teacher_id:
        return {"error": "Permission denied"}

    db_teacher.first_name = teacher.first_name
    db_teacher.last_name = teacher.last_name
    db_teacher.email = teacher.email
    db_teacher.phone = teacher.phone
    db_teacher.faculty = teacher.faculty

    db.commit()
    db.refresh(db_teacher)

    return db_teacher


# ======================
# ลบอาจารย์ (ลบได้เฉพาะตัวเอง)
# ======================
@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    login_teacher_id: int = Query(...),
    db: Session = Depends(get_db)
):

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.teacher_id == teacher_id
    ).first()

    if not db_teacher:
        return {"error": "Teacher not found"}

    # เช็คสิทธิ์
    if teacher_id != login_teacher_id:
        return {"error": "Permission denied"}

    db.delete(db_teacher)
    db.commit()

    return {"message": "Teacher deleted successfully"}