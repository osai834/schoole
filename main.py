from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List
from fastapi.staticfiles import StaticFiles
from db import SessionLocal, Student, Lesson, Enrollment

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# Database
# ==========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# Pydantic Models
# ==========================

class StudentBody(BaseModel):
    name: str
    phone: str
    age: int


class StudentResponse(BaseModel):
    id: int
    name: str
    phone: str
    age: int

    model_config = ConfigDict(from_attributes=True)


class LessonBody(BaseModel):
    title: str
    teacher: str


class LessonResponse(BaseModel):
    id: int
    title: str
    teacher: str

    model_config = ConfigDict(from_attributes=True)


class EnrollmentBody(BaseModel):
    student_id: int
    lesson_id: int


# ==========================
# Students CRUD
# ==========================

# عرض جميع الطلاب
@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# إضافة طالب
@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentBody, db: Session = Depends(get_db)):

    new_student = Student(
        name=student.name,
        phone=student.phone,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# تعديل طالب
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentBody,
    db: Session = Depends(get_db)
):

    old_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not old_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    old_student.name = student.name
    old_student.phone = student.phone
    old_student.age = student.age

    db.commit()
    db.refresh(old_student)

    return old_student


# حذف طالب
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted"}


# ==========================
# Lessons CRUD
# ==========================

# عرض جميع الدروس
@app.get("/lessons", response_model=List[LessonResponse])
def get_lessons(
    db: Session = Depends(get_db)
):
    return db.query(Lesson).all()


# إضافة درس
@app.post("/lessons", response_model=LessonResponse)
def create_lesson(
    lesson: LessonBody,
    db: Session = Depends(get_db)
):

    new_lesson = Lesson(
        title=lesson.title,
        teacher=lesson.teacher
    )

    db.add(new_lesson)

    db.commit()

    db.refresh(new_lesson)

    return new_lesson


# تعديل درس
@app.put("/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson: LessonBody,
    db: Session = Depends(get_db)
):

    old_lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not old_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    old_lesson.title = lesson.title
    old_lesson.teacher = lesson.teacher

    db.commit()

    db.refresh(old_lesson)

    return old_lesson


# حذف درس
@app.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    db.delete(lesson)

    db.commit()

    return {"message": "Lesson deleted"}
# ==========================
# Enrollment Response
# ==========================

class EnrollmentResponse(BaseModel):
    id: int
    student: str
    lesson: str
    teacher: str


# ==========================
# Enrollments CRUD
# ==========================

# عرض جميع التسجيلات
@app.get(
    "/enrollments",
    response_model=List[EnrollmentResponse]
)
def get_enrollments(
    db: Session = Depends(get_db)
):

    enrollments = db.query(Enrollment).all()

    result = []

    for item in enrollments:

        result.append(
            EnrollmentResponse(
                id=item.id,
                student=item.student.name,
                lesson=item.lesson.title,
                teacher=item.lesson.teacher
            )
        )

    return result


# تسجيل طالب في درس
@app.post("/enrollments")
def create_enrollment(
    enrollment: EnrollmentBody,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    lesson = db.query(Lesson).filter(
        Lesson.id == enrollment.lesson_id
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    exists = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.lesson_id == enrollment.lesson_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Enrollment already exists"
        )

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        lesson_id=enrollment.lesson_id
    )

    db.add(new_enrollment)

    db.commit()

    db.refresh(new_enrollment)

    return {
        "message": "Enrollment created"
    }


# حذف تسجيل
@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):

    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    db.delete(enrollment)

    db.commit()

    return {
        "message": "Enrollment deleted"
    }


# ==========================
# Run Server
# ==========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
