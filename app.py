#Corey Scott CIT 257 Program 5
from flask import Flask, render_template, request,url_for,flash
from models import *

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =  'random string'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

#get information course information route
@app.route("/courseInfo", methods=["POST"])
def courseInfo():
    
    cid = request.form.get('courses')

    course = Course.query.filter_by(course_id=cid).first()
    return render_template('courseInfo.html',course=course)

#remove student from class route
@app.route('/remove',methods=['GET'])
def remove():
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')
   

    s = Student.query.get(student_id)
    c = Course.query.get(course_id)
            
    
    s.sched.remove(c)
    db.session.commit()


    return render_template('sucess.html', name = s.student_name,message="was removed from the class")



#add student to class route
@app.route('/addroster', methods=["POST"])
def addroster():
    cid = request.form.get('courseNum')
    sid = request.form.get('studentId')
    

    s = Student.query.get(sid)
    c = Course.query.get(cid)

    
    #there are some id's that aren't in the database
    if not s:
        return render_template('error.html', message="That student ID is not in the database")
    
    if not s in c.student:
        c.student.append(s)
        db.session.commit()
        return render_template('sucess.html', name= s.student_name, message="Has been added to the class")
    
        
    return render_template('error.html', message="That student is already in the class")


@app.route('/searchStudent')
def searchStudent():
    return render_template('studentSearch.html')


#get student information route
@app.route('/studentInfo',methods=["POST"])
def studentinfo():
    sid = request.form.get('studentId')
    if not Student.query.get(sid):
        return render_template('error.html', message='that id is not in the database')
    info = Student.query.filter_by(student_id=sid).first()

    return render_template('studentInfo.html',info = info)



#add student to database route
@app.route('/newStudent',methods=["POST" ,"GET"])
def newStudent():
    if request.method == "GET":
        return render_template('newStudent.html')
    stuName= request.form.get('studentName')
    stuEmail = request.form.get('studentEmail')

    newstu = Student(student_name = stuName,email = stuEmail)

    db.session.add(newstu)
    db.session.commit()

    
    return render_template('sucess.html',name = stuName, message="Was succesfully registered")  





if __name__ == "__main__":
    db.create_all()