from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from datetime import datetime
from dependencies import get_current_user

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

# ======================
# ดูอาจารย์ทั้งหมด (ทุก role ดูได้)
# ======================
@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()


# ======================
# เพิ่มอาจารย์ (เฉพาะ teacher เท่านั้น)
# ======================
@router.post("/")
def create_teacher(
    teacher: schemas.TeacherCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Permission denied"}

    new_teacher = models.Teacher(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        email=teacher.email,
        phone=teacher.phone,
        faculty=teacher.faculty
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
    role: str = Query(...),
    login_teacher_id: int = Query(...),
    db: Session = Depends(get_db)
):

    if role != "teacher":
        return {"error": "Students cannot edit teachers"}

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.teacher_id == teacher_id
    ).first()

    if not db_teacher:
        return {"error": "Teacher not found"}

    # เช็คว่าเป็นเจ้าของข้อมูล
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
    role: str = Query(...),
    login_teacher_id: int = Query(...),
    db: Session = Depends(get_db)
):

    if role != "teacher":
        return {"error": "Students cannot delete teachers"}

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.teacher_id == teacher_id
    ).first()

    if not db_teacher:
        return {"error": "Teacher not found"}

    if teacher_id != login_teacher_id:
        return {"error": "Permission denied"}

    db.delete(db_teacher)
    db.commit()

    return {"message": "Teacher deleted successfully"}