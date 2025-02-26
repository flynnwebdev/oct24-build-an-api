from init import db, ma
from marshmallow_sqlalchemy import fields

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250))

    courses = db.relationship('Course', back_populates='teacher')


class TeacherSchema(ma.Schema):
    courses = fields.Nested('CourseSchema', many=True, exclude=['teacher', 'teacher_id'])

    class Meta:
        fields = ('id', 'name', 'department', 'address', 'courses')


one_teacher = TeacherSchema()
many_teachers = TeacherSchema(many=True)

teacher_without_id = TeacherSchema(exclude=['id'])
