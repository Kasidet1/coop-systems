from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from datetime import datetime

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

# GET teachers
@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()

# POST teacher
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