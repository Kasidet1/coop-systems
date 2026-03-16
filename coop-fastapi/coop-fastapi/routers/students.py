from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas
from dependencies import get_current_user

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# ======================
# ดูข้อมูลนักศึกษา
# ======================
@router.get("/")
def get_students(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # teacher ดูได้ทั้งหมด
    if current_user["role"] == "teacher":
        return db.query(models.Student).all()

    # student ดูเฉพาะตัวเอง
    if current_user["role"] == "student":
        return db.query(models.Student).filter(
            models.Student.student_id == current_user["username"]
        ).first()

    return {"error": "invalid role"}


# ======================
# เพิ่มนักศึกษา (Teacher เท่านั้น)
# ======================
@router.post("/")
def create_student(
    student: schemas.StudentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can create student"}

    new_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        phone=student.phone,
        faculty=student.faculty,
        major=student.major,
        year=student.year,
        created_at=datetime.now()
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ======================
# แก้ไขข้อมูลนักศึกษา
# ======================
@router.put("/{student_id}")
def update_student(
    student_id: str,
    student: schemas.StudentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not db_student:
        return {"error": "Student not found"}

    # student แก้ได้เฉพาะตัวเอง
    if current_user["role"] == "student" and student_id != current_user["username"]:
        return {"error": "Permission denied"}

    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.email = student.email
    db_student.phone = student.phone
    db_student.faculty = student.faculty
    db_student.major = student.major
    db_student.year = student.year

    db.commit()
    db.refresh(db_student)

    return db_student


# ======================
# ลบนักศึกษา
# ======================
@router.delete("/{student_id}")
def delete_student(
    student_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not db_student:
        return {"error": "Student not found"}

    # student ลบได้เฉพาะตัวเอง
    if current_user["role"] == "student" and student_id != current_user["username"]:
        return {"error": "Permission denied"}

    db.delete(db_student)
    db.commit()

    return {"message": "Student deleted successfully"}