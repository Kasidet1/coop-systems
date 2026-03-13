from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

# ดูบริษัททั้งหมด
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()


# เพิ่มบริษัท
@router.post("/")
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):

    new_company = models.Company(
        company_name=company.company_name,
        contact_person=company.contact_person,
        email=company.email,
        phone=company.phone,
        address=company.address,
        created_at=datetime.now()
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company