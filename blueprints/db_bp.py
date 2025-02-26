from flask import Blueprint
from init import db
from datetime import date
from models.student import Student
from models.teacher import Teacher
from models.course import Course

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables created')

@db_bp.cli.command('seed')
def seed_tables():
    students = [
        Student(
            name='Mary Jones',
            email='mary.jones@gmail.com',
            address='Sydney'
        ),
        Student(
            name='John Smith',
            email='john.smith@outlook.com',
        )
    ]

    teachers = [
        Teacher(
            name='Mr. Robot',
            department='Training and Development',
            address='Brisbane'
        ),
        Teacher(
            name='Alex Holder',
            department='Training and Development',
            address='Sydney'
        )
    ]

    db.session.add_all(teachers)
    db.session.commit()

    courses = [
        Course(
            name='Diploma of Web Development',
            start_date=date(2025, 10, 1),
            end_date=date(2026, 4, 20),
            teacher=teachers[1]
        ),
        Course(
            name='Diploma of Cybersecurity',
            start_date=date(2026, 1, 14),
            end_date=date(2026, 7, 10),
            teacher=teachers[0]
        )
    ]

    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.commit()
    print('Tables seeded')
