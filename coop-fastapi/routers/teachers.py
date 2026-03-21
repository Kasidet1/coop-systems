from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from dependencies import get_current_user

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

# ======================
# ดูข้อมูลอาจารย์
# ======================
@router.get("/me")
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    teacher = db.query(models.Teacher).filter(
        models.Teacher.username == current_user["username"]
    ).first()

    if not teacher:
        return {"message": "Profile not created"}

    return teacher


# ======================
# เพิ่ม / แก้ข้อมูลตัวเอง
# ======================
@router.put("/me")
def update_my_profile(
    teacher: schemas.TeacherCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.username == current_user["username"]
    ).first()

    # ถ้ายังไม่มี → สร้าง
    if not db_teacher:

        db_teacher = models.Teacher(
            username=current_user["username"],
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            email=teacher.email,
            phone=teacher.phone,
            faculty=teacher.faculty
        )

        db.add(db_teacher)

    # ถ้ามีแล้ว → update
    else:

        db_teacher.first_name = teacher.first_name
        db_teacher.last_name = teacher.last_name
        db_teacher.email = teacher.email
        db_teacher.phone = teacher.phone
        db_teacher.faculty = teacher.faculty

    db.commit()
    db.refresh(db_teacher)

    return db_teacher


# ======================
# ลบข้อมูลตัวเอง
# ======================
@router.delete("/me")
def delete_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_teacher = db.query(models.Teacher).filter(
        models.Teacher.username == current_user["username"]
    ).first()

    if not db_teacher:
        return {"error": "Profile not found"}

    db.delete(db_teacher)
    db.commit()

    return {"message": "Profile deleted successfully"}