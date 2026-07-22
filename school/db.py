from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///academy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ==========================
# Student Model
# ==========================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    age = Column(Integer)

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete"
    )


# ==========================
# Lesson Model
# ==========================

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    teacher = Column(String)

    enrollments = relationship(
        "Enrollment",
        back_populates="lesson",
        cascade="all, delete"
    )


# ==========================
# Enrollment Model
# ==========================

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id")
    )

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    lesson = relationship(
        "Lesson",
        back_populates="enrollments"
    )


Base.metadata.create_all(bind=engine)