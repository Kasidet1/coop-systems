from fastapi import FastAPI
from pydantic import BaseModel
from routers import students, companies, requests, notifications, schedule, documents, reports

app = FastAPI(title="Coop System API")

# ======================
# Login Model
# ======================
class Login(BaseModel):
    username: str
    password: str

# ======================
# Login API
# ======================
@app.post("/login")
def login(data: Login):
    if data.username == "admin" and data.password == "1234":
        return {
            "message": "login success",
            "role": "admin"
        }
    else:
        return {
            "message": "invalid username or password"
        }

# ======================
# Routers
# ======================
app.include_router(students.router)
app.include_router(companies.router)
app.include_router(requests.router)
app.include_router(notifications.router)
app.include_router(schedule.router)
app.include_router(documents.router)
app.include_router(reports.router)