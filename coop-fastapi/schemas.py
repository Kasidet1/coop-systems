from pydantic import BaseModel

class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    major: str
    year: int

class CompanyCreate(BaseModel):
    company_name: str
    address: str

class RequestCreate(BaseModel):
    student_id: str
    company_id: int
    status: str