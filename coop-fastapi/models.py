from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(String(10), primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    faculty = Column(String(100))
    major = Column(String(100))
    year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    faculty = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200))
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class InternshipRequest(Base):
    __tablename__ = "internship_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(10), ForeignKey("students.student_id"))
    company_name = Column(String(200))
    status = Column(String(50), default="รอการอนุมัติ")
    created_at = Column(TIMESTAMP, server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(10), ForeignKey("students.student_id"))
    title = Column(String(200))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)


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