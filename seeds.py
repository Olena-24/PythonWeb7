from faker import Faker
from connect_db import session, engine
from models import Student, Group, Subject, Teacher, Grade, Base
import random

fake = Faker()

NUMBER_STUDENTS = random.randint(30, 50)
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = random.randint(5, 8)
NUMBER_TEACHERS = random.randint(3, 5)
NUMBER_GRADES = 20

law_subjects = [
    "Цивільне право",
    "Кримінальне право",
    "Конституційне право",
    "Міжнародне право",
    "Трудове право"
]

def add_law_subjects():
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(first_name=fake.first_name(), last_name=fake.last_name())
        session.add(teacher)
    session.commit()

    for subject_name in law_subjects[:NUMBER_SUBJECTS]:
        subject = Subject(subject_name=subject_name, teacher_id=random.randint(1, NUMBER_TEACHERS))
        session.add(subject)
    session.commit()

def add_groups():
    for i in range(1, NUMBER_GROUPS + 1):
        group_name = f"{i}-я група"
        group = Group(group_name=group_name)
        session.add(group)
    session.commit()
    
def add_students(number_of_students: int):
    groups = session.query(Group).all()  # Отримання всіх груп з бази даних
    for _ in range(number_of_students):
        first_name = fake.first_name()
        last_name = fake.last_name()
        group = random.choice(groups)  # Вибір випадкової групи зі списку
        student = Student(first_name=first_name, last_name=last_name, group=group)
        session.add(student)
    session.commit()

def add_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for _ in range(NUMBER_GRADES):
            grade = Grade(
                student_id=student.id,
                subject_id=random.choice(subjects).id,
                grade=random.randint(0, 100),
                grade_date=fake.date_this_year()
            )
            session.add(grade)
    session.commit()

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    add_law_subjects()
    add_groups()
    add_students(NUMBER_STUDENTS)
    add_grades()
    print("Дані успішно додані до бази даних.")