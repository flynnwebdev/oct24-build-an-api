from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.course import Course, many_courses, one_course, course_without_id

courses_bp = Blueprint('courses', __name__)

# Read all - GET /courses
@courses_bp.route('/courses')
def get_all_courses():
    stmt = db.select(Course).order_by(Course.name)
    courses = db.session.scalars(stmt)
    return many_courses.dump(courses)

# Read one - GET /courses/<int:id>
@courses_bp.route('/courses/<int:course_id>')
def get_one_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        return one_course.dump(course)
    else:
        return {'error': f'Course with id {course_id} does not exist'}, 404
    
# Create - POST /courses
@courses_bp.route('/courses', methods=['POST'])
def create_course():
    try:
        # Get incoming request body (JSON)
        data = course_without_id.load(request.json)
        # Create a new instance of Course model
        new_course = Course(
            name=data.get('name'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            teacher_id=data.get('teacher_id')
        )
        # Add the instance to the db session
        db.session.add(new_course)
        # Commit the session
        db.session.commit()
        # Return the new Course instance
        return one_course.dump(new_course), 201
    except Exception as err:
        return {"error": str(err)}, 400


# Update - PUT /courses/<int:id>
@courses_bp.route('/courses/<int:course_id>', methods=['PUT', 'PATCH'])
def update_course(course_id):
    try:
        # Fetch the course by id
        stmt = db.select(Course).filter_by(id=course_id)
        course = db.session.scalar(stmt)
        if course:
            # Get incoming request body (JSON)
            data = course_without_id.load(request.json)
            # Update the attributes of the course with the incoming data
            course.name = data.get('name') or course.name
            course.start_date = data.get('start_date') or course.start_date
            course.end_date = data.get('end_date') or course.end_date
            course.teacher_id = data.get('teacher_id', course.teacher_id)
            # Commit the session
            db.session.commit()
            # Return the new Course instance
            return one_course.dump(course)
        else:
            return {'error': f'Course with id {course_id} does not exist'}, 404 
    except Exception as err:
        return {"error": str(err)}, 400


# Delete - DELETE /courses/<int:id>
@courses_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        db.session.delete(course)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Course with id {course_id} does not exist'}, 404 
   

