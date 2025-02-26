from init import db, ma
from marshmallow_sqlalchemy import fields

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='courses')


class CourseSchema(ma.Schema):
    teacher = fields.Nested('TeacherSchema')

    class Meta:
        fields = ('id', 'name', 'start_date', 'end_date', 'teacher_id', 'teacher')


one_course = CourseSchema()
many_courses = CourseSchema(many=True, exclude=['teacher'])

course_without_id = CourseSchema(exclude=['id'])
