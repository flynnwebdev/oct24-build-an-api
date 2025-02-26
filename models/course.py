from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String
from marshmallow.validate import Length, Regexp, And

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='courses')


class CourseSchema(ma.Schema):
    name = String(required=True, validate=And(
        Length(min=5, error='Name must be at least 5 characters long'),
        Regexp('^[A-Za-z0-9 ()]$', error='Only letters, numbers, spaces and parentheses allowed')
    ))

    teacher = fields.Nested('TeacherSchema')

    class Meta:
        fields = ('id', 'name', 'start_date', 'end_date', 'teacher_id', 'teacher')


one_course = CourseSchema()
many_courses = CourseSchema(many=True, exclude=['teacher'])

course_without_id = CourseSchema(exclude=['id'])
