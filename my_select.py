from sqlalchemy import func
from connect_db import session
from models import Student, Group, Grade, Teacher, Subject

# Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    return session.query(
        Student.first_name, Student.last_name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()

# Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_id):
    return session.query(
        Student.first_name, Student.last_name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()

# Знайти середній бал у групах з певного предмета
def select_3(subject_id):
    return session.query(
        Group.group_name, func.avg(Grade.grade).label('average_grade')
    ).join(Student, Group.id == Student.group_id).join(Grade, Student.id == Grade.student_id).filter(Grade.subject_id == subject_id).group_by(Group.group_name).all()

# Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    return session.query(
        func.avg(Grade.grade).label('average_grade')
    ).scalar()

# Знайти які курси читає певний викладач
def select_5(teacher_id):
    return session.query(
        Subject.subject_name  # Используйте 'subject_name' вместо 'name'
    ).filter(Subject.teacher_id == teacher_id).all()

# Знайти список студентів у певній групі
def select_6(group_id):
    return session.query(
        Student.first_name, Student.last_name
    ).filter(Student.group_id == group_id).all()

# Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_id, subject_id):
    return session.query(
        Student.first_name, Student.last_name, Grade.grade
    ).join(Group).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()

# Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_id):
    return session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()

# Знайти список курсів, які відвідує певний студент
def select_9(student_id):
    student_courses = session.query(
        Subject.subject_name
    ).join(Grade).join(Student).filter(Student.id == student_id).distinct().all()
    return student_courses

# Список курсів, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    return session.query(
        Subject.subject_name
    ).join(Grade).join(Teacher).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).distinct().all()
if __name__ == '__main__':
    # Пример вызова функций и вывод результатов в консоль
    print("Знайти 5 студентів із найбільшим середнім балом з усіх предметів:")
    print(select_1())
    
    print("\nЗнайти студента із найвищим середнім балом з певного предмета:")
    print(select_2(subject_id=1))
    
    print("\nЗнайти середній бал у групах з певного предмета:")
    print(select_3(subject_id=3))
    
    print("\nЗнайти середній бал на потоці (по всій таблиці оцінок):")
    print(select_4())
    
    print("\nЗнайти які курси читає певний викладач:")
    print(select_5(teacher_id=1))
    
    print("\nЗнайти список студентів у певній групі:")
    print(select_6(group_id=2))
    
    print("\nЗнайти оцінки студентів у окремій групі з певного предмета:")
    print(select_7(group_id=3, subject_id=3))
    
    print("\nЗнайти середній бал, який ставить певний викладач зі своїх предметів:")
    print(select_8(teacher_id=1))
    
    print("\nЗнайти список курсів, які відвідує певний студент:")
    print(select_9(student_id=7))
    
    print("\nСписок курсів, які певному студенту читає певний викладач:")
    print(select_10(student_id=7, teacher_id=1))