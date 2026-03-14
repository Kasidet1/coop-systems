from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

# ======================
# ดูบริษัททั้งหมด
# ======================
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()


# ======================
# เพิ่มบริษัท (Teacher เท่านั้น)
# ======================
@router.post("/")
def create_company(
    company: schemas.CompanyCreate,
    role: str = Query(...),
    db: Session = Depends(get_db)
):

    if role != "teacher":
        return {"error": "Only teacher can add company"}

    new_company = models.Company(
        company_name=company.company_name,
        contact_person=company.contact_person,
        email=company.email,
        phone=company.phone,
        address=company.address,
        position=company.position,
        created_at=datetime.now()
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


# ======================
# แก้ไขบริษัท (Teacher เท่านั้น)
# ======================
@router.put("/{company_id}")
def update_company(
    company_id: int,
    company: schemas.CompanyCreate,
    role: str = Query(...),
    db: Session = Depends(get_db)
):

    if role != "teacher":
        return {"error": "Only teacher can update company"}

    db_company = db.query(models.Company).filter(
        models.Company.company_id == company_id
    ).first()

    if not db_company:
        return {"error": "Company not found"}

    db_company.company_name = company.company_name
    db_company.contact_person = company.contact_person
    db_company.email = company.email
    db_company.phone = company.phone
    db_company.address = company.address
    db_company.position = company.position

    db.commit()
    db.refresh(db_company)

    return db_company


# ======================
# ลบบริษัท (Teacher เท่านั้น)
# ======================
@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    role: str = Query(...),
    db: Session = Depends(get_db)
):

    if role != "teacher":
        return {"error": "Only teacher can delete company"}

    db_company = db.query(models.Company).filter(
        models.Company.company_id == company_id
    ).first()

    if not db_company:
        return {"error": "Company not found"}

    db.delete(db_company)
    db.commit()

    return {"message": "Company deleted successfully"}