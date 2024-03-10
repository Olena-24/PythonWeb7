from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(255), nullable=False, unique=True)

    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)

    group = relationship("Group", back_populates="students")

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

Group.students = relationship("Student", order_by=Student.id, back_populates="group")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150))
    last_name = Column(String(150))

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(175))
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))

    teacher = relationship("Teacher", back_populates="subjects")

Teacher.subjects = relationship("Subject", order_by=Subject.id, back_populates="teacher")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))
    grade = Column(Integer, nullable=False)  # Виправлено оголошення колонки grade
    grade_date = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

Student.grades = relationship("Grade", order_by=Grade.id, back_populates="student")
Subject.grades = relationship("Grade", order_by=Grade.id, back_populates="subject")

# Налаштування бази даних та створення таблиць
engine = create_engine('sqlite:///data_sql.db', echo=True)
Base.metadata.create_all(engine)