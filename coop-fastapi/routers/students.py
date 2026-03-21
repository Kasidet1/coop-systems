from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from dependencies import get_current_user

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# ======================
# ดูข้อมูลตัวเอง (Student)
# ======================
@router.get("/me", response_model=schemas.StudentResponse)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == current_user["username"]
    ).first()

    if not student:
        return {
            "student_id": current_user["username"],
            "first_name": "student",
            "last_name": "",
            "email": "",
            "phone": "",
            "faculty": "",
            "major": "",
            "year": None,
            "status": "รอนิเทศ",
            "company_name": None,
            "week": None
        }

    return student

# ======================
# ดูนักศึกษาทั้งหมด (Admin / Teacher) เฉพาะนักศึกษาที่ company_name ไม่ใช่ None
# ======================
@router.get("/all", response_model=list[schemas.StudentResponse])
def get_all_students(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Filter เฉพาะนักศึกษาที่ admin อนุมัติ company_name แล้ว
    students = db.query(models.Student).filter(models.Student.company_name != None).all()
    return students

# ======================
# ดูนักศึกษารายคน
# ======================
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student_by_id(
    student_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ======================
# แก้ไขข้อมูลนักศึกษา (เฉพาะ Student)
# ======================
@router.put("/{student_id}", response_model=schemas.StudentResponse)
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
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only student can update profile")
    if student_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="You can update only your profile")

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
# ลบข้อมูลนักศึกษา (เฉพาะ Student)
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
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only student can delete profile")
    if student_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="You can delete only your profile")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

# ======================
# Teacher / Admin อัปเดตสถานะนิเทศ
# ======================
@router.put("/{student_id}/status", response_model=schemas.StudentResponse)
def update_internship_status(
    student_id: str,
    status: schemas.InternshipStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Only teacher/admin can update status")

    db_student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.status = status.status
    db.commit()
    db.refresh(db_student)

    return db_student