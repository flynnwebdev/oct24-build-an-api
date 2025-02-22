from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teacher import Teacher, many_teachers, one_teacher, teacher_without_id

teachers_bp = Blueprint('teachers', __name__)

# Read all - GET /teachers
@teachers_bp.route('/teachers')
def get_all_teachers():
    stmt = db.select(Teacher).order_by(Teacher.name)
    teachers = db.session.scalars(stmt)
    return many_teachers.dump(teachers)

# Read one - GET /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>')
def get_one_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return one_teacher.dump(teacher)
    else:
        return {'error': f'Teacher with id {teacher_id} does not exist'}, 404
    
# Create - POST /teachers
@teachers_bp.route('/teachers', methods=['POST'])
def create_teacher():
    try:
        # Get incoming request body (JSON)
        data = teacher_without_id.load(request.json)
        # Create a new instance of Teacher model
        new_teacher = Teacher(
            name=data.get('name'),
            department=data.get('department'),
            address=data.get('address')
        )
        # Add the instance to the db session
        db.session.add(new_teacher)
        # Commit the session
        db.session.commit()
        # Return the new Teacher instance
        return one_teacher.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409 # Conflict
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     return {"error": str(err.orig)}, 400
        else:
            return {"error": str(err.orig)}, 400


# Update - PUT /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['PUT', 'PATCH'])
def update_teacher(teacher_id):
    try:
        # Fetch the teacher by id
        stmt = db.select(Teacher).filter_by(id=teacher_id)
        teacher = db.session.scalar(stmt)
        if teacher:
            # Get incoming request body (JSON)
            data = teacher_without_id.load(request.json)
            # Update the attributes of the teacher with the incoming data
            teacher.name = data.get('name') or teacher.name
            teacher.department = data.get('department') or teacher.department
            teacher.address = data.get('address', teacher.address)
            # Commit the session
            db.session.commit()
            # Return the new Teacher instance
            return one_teacher.dump(teacher)
        else:
            return {'error': f'Teacher with id {teacher_id} does not exist'}, 404 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409 # Conflict
        else:
            return {"error": str(err.orig)}, 400


# Delete - DELETE /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Teacher with id {teacher_id} does not exist'}, 404 
   

# Possible extra routes:
# Enrol - POST /teachers/<int:teacher_id>/<int:course_id>
# Unenrol - DELETE /teachers/<int:teacher_id>/<int:course_id>
