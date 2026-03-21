from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil

from database import get_db
from dependencies import get_current_user
import models

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

UPLOAD_FOLDER = "report_files/teachers"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ======================
# ดูรายงานทั้งหมด
# ======================
@router.get("/")
def get_reports(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] not in ["teacher", "admin"]:
        return {"error": "Permission denied"}

    return db.query(models.Report).all()


# ======================
# ดูรายงานของนักศึกษา
# ======================
@router.get("/student/{student_id}")
def get_student_reports(
    student_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] not in ["teacher", "admin"]:
        return {"error": "Permission denied"}

    return db.query(models.Report).filter(
        models.Report.student_id == student_id
    ).all()


# ======================
# เพิ่มรายงาน + upload file
# ======================
@router.post("/")
def create_report(
    student_id: str = Form(...),
    teacher_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can create report"}

    teacher_name = current_user["username"]

    # สร้างโฟลเดอร์ teacher
    teacher_folder = f"{UPLOAD_FOLDER}/{teacher_name}"
    os.makedirs(teacher_folder, exist_ok=True)

    # สร้างโฟลเดอร์ student
    student_folder = f"{teacher_folder}/{student_id}"
    os.makedirs(student_folder, exist_ok=True)

    file_path = f"{student_folder}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_report = models.Report(
        student_id=student_id,
        teacher_id=teacher_id,
        title=title,
        description=description,
        file_url=file_path,
        submitted_at=datetime.now()
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report uploaded successfully",
        "data": new_report
    }


# ======================
# แก้ไขรายงาน
# ======================
@router.put("/{report_id}")
def update_report(
    report_id: int,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can update report"}

    report = db.query(models.Report).filter(
        models.Report.report_id == report_id
    ).first()

    if not report:
        return {"error": "Report not found"}

    report.title = title
    report.description = description

    if file:

        teacher_name = current_user["username"]

        teacher_folder = f"{UPLOAD_FOLDER}/{teacher_name}"
        os.makedirs(teacher_folder, exist_ok=True)

        student_folder = f"{teacher_folder}/{report.student_id}"
        os.makedirs(student_folder, exist_ok=True)

        file_path = f"{student_folder}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        report.file_url = file_path

    db.commit()
    db.refresh(report)

    return report


# ======================
# ลบรายงาน
# ======================
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can delete report"}

    report = db.query(models.Report).filter(
        models.Report.report_id == report_id
    ).first()

    if not report:
        return {"error": "Report not found"}

    if report.file_url and os.path.exists(report.file_url):
        os.remove(report.file_url)

    db.delete(report)
    db.commit()

    return {"message": "Report deleted successfully"}