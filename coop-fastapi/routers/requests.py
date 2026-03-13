from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from utils.notification_service import create_notification
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/requests",
    tags=["Internship Requests"]
)

# ดูคำร้อง
@router.get("/")
def get_requests(
    role: str = Query(...), 
    student_id: str = Query(None),
    db: Session = Depends(get_db)
):

    # ถ้าเป็นอาจารย์ → ดูทั้งหมด
    if role == "teacher":
        return db.query(models.InternshipRequest).all()

    # ถ้าเป็นนักศึกษา → ดูเฉพาะของตัวเอง
    elif role == "student":
        return db.query(models.InternshipRequest).filter(
            models.InternshipRequest.student_id == student_id
        ).all()

    return {"error": "invalid role"}


# นักศึกษายื่นคำร้อง
@router.post("/")
def create_request(data: schemas.RequestCreate, db: Session = Depends(get_db)):

    new_request = models.InternshipRequest(
        student_id=data.student_id,
        company_name=data.company_name,
        status="รอการอนุมัติ"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # สร้าง notification
    create_notification(
        db,
        data.student_id,
        f"คุณได้ยื่นคำร้องฝึกงานกับบริษัท {data.company_name}"
    )

    return new_request

router = APIRouter(
    prefix="/requests",
    tags=["Internship Requests"]
)

# ดูคำร้อง
@router.get("/")
def get_requests(
    role: str = Query(...), 
    student_id: str = Query(None),
    db: Session = Depends(get_db)
):

    # ถ้าเป็นอาจารย์ → ดูทั้งหมด
    if role == "teacher":
        return db.query(models.InternshipRequest).all()

    # ถ้าเป็นนักศึกษา → ดูเฉพาะของตัวเอง
    elif role == "student":
        return db.query(models.InternshipRequest).filter(
            models.InternshipRequest.student_id == student_id
        ).all()

    return {"error": "invalid role"}


@router.put("/{request_id}/approve")
def approve_request(request_id: int, db: Session = Depends(get_db)):

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()

    request.status = "อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณได้รับการอนุมัติ"
    )

    return {"message": "อนุมัติเรียบร้อย"}

@router.put("/{request_id}/reject")
def reject_request(request_id: int, db: Session = Depends(get_db)):

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()

    request.status = "ไม่อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณไม่ได้รับการอนุมัติ"
    )

    return {"message": "ไม่อนุมัติ"}