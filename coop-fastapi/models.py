from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    faculty = Column(String)
    major = Column(String)
    year = Column(Integer)

    # เพิ่ม 2 field นี้
    company_name = Column(String, nullable=True)  # บริษัทที่อนุมัติแล้ว
    status = Column(String, default="รอนิเทศ")   # สถานะนิเทศ


class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    faculty = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Company(Base):
    __tablename__ = "companies"
    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    position = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class InternshipRequest(Base):
    __tablename__ = "internship_requests"
    request_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False)
    student_name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=True)
    company_name = Column(String)
    status = Column(String, default="รอการอนุมัติ")
    created_at = Column(TIMESTAMP, server_default=func.now())


    company = relationship("Company", backref="requests")

    # join relationship
    company = relationship("Company", backref="requests")


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(10), ForeignKey("students.student_id"))
    title = Column(String(200))
    file_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(10), ForeignKey("students.student_id"))
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))
    title = Column(String(200))
    description = Column(Text)
    file_url = Column(String(255))
    submitted_at = Column(TIMESTAMP, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50))


class LoginLog(Base):
    __tablename__ = "login_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    role = Column(String(50))
    login_time = Column(TIMESTAMP, server_default=func.now())