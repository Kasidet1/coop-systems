from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# GET students
@router.get("/")
def get_students(
    role: str = Query(...),
    student_id: str = Query(None),
    db: Session = Depends(get_db)
):

    # อาจารย์ดูได้ทั้งหมด
    if role == "teacher":
        return db.query(models.Student).all()

    # นักศึกษาดูได้เฉพาะตัวเอง
    elif role == "student":
        return db.query(models.Student).filter(
            models.Student.student_id == student_id
        ).first()

    return {"error": "invalid role"}


# POST student
@router.post("/")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):

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