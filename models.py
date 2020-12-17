from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


student_association = db.Table('student_association',
    db.Column('course_id',db.Integer,db.ForeignKey('course.course_id')),
    db.Column('student_id',db.Integer,db.ForeignKey('student.student_id'))
)

class Course(db.Model):
    course_id = db.Column(db.Integer,primary_key=True)
    course_number = db.Column(db.Integer,nullable=False)
    course_name = db.Column(db.String,nullable=False)
    student = db.relationship("Student", secondary=student_association, backref=db.backref('sched'),lazy='dynamic')

class Student(db.Model):
    student_id = db.Column(db.Integer,primary_key =True)
    student_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)    
