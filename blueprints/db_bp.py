from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher

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

    db.session.add_all(students)
    db.session.add_all(teachers)
    db.session.commit()
    print('Tables seeded')
