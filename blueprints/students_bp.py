from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.student import Student, many_students, one_student, student_without_id

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student)
    students = db.session.scalars(stmt)
    return many_students.dump(students)

# Read one - GET /students/<int:id>
@students_bp.route('/students/<int:student_id>')
def get_one_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        return one_student.dump(student)
    else:
        return {'error': f'Student with id {student_id} does not exist'}, 404
    
# Create - POST /students
@students_bp.route('/students', methods=['POST'])
def create_student():
    try:
        # Get incoming request body (JSON)
        data = student_without_id.load(request.json)
        # Create a new instance of Student model
        new_student = Student(
            name=data.get('name'),
            email=data.get('email'),
            address=data.get('address')
        )
        # Add the instance to the db session
        db.session.add(new_student)
        # Commit the session
        db.session.commit()
        # Return the new Student instance
        return one_student.dump(new_student), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409 # Conflict
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": "Field is required"}, 400
        else:
            return {"error": err._message()}, 400


# Update - PUT /students/<int:id>
# Delete - DELETE /students/<int:id>

# Possible extra routes:
# Enrol - POST /students/<int:student_id>/<int:course_id>
# Unenrol - DELETE /students/<int:student_id>/<int:course_id>
