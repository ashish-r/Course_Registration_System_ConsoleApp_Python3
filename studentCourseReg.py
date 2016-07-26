import sqlite3

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def create_course_student_table():
    curr.execute("CREATE TABLE IF NOT EXISTS course_student(c_id INTEGER, s_id INTEGER, marks INTEGER, certificate BOOLEAN DEFAULT FALSE )")

def create_courses_table():
    curr.execute("CREATE TABLE IF NOT EXISTS courses(c_id INTEGER, c_name TEXT, c_description TEXT, c_startdate DATE, c_enddate DATE, c_teacherid INTEGER)")

def view_registered_courses(sid):
    curr.execute("select course_student.c_id,courses.c_name, courses.c_startdate from  course_student,courses where course_student.c_id = courses.c_id and course_student.s_id=:s_id",{"s_id": sid})
    conn.commit()
    rcourses = curr.fetchall()
    print("COURSES ARE:")
    print(" CID  - CNAME - Start Date")
    for rcourse in rcourses:
        print(rcourse[0], ' - ', rcourse[1], ' - ', rcourse[2])
    avlCourseId = [int(i[0]) for i in rcourses]

    while True:
        print("=================================================================================")
        print('Or Enter Course Id For Details')
        print('Or Enter 0000 to go back')
        c_idChoice = int(input('Enter: '))
        if c_idChoice == 0000:
            return
        elif c_idChoice in avlCourseId:
            view_reg_course_detail(c_idChoice)
        else:
            print('CHOOSE CORRECT OPTION \n')

def view_reg_course_detail(cid):
    curr.execute("SELECT courses.c_id, courses.c_name, courses.c_description, courses.c_startdate, courses.c_enddate, course_student.marks, course_student.certificate, teachers.t_id, teachers.t_name  from courses,course_student,teachers where courses.c_id=:c_id and courses.c_id = course_student.c_id  and teachers.t_id = courses.c_teacherid", {"c_id": cid})
    conn.commit()
    courseDetail = curr.fetchone()

    print('Course ID: ', courseDetail[0], ' Course Name: ', courseDetail[1])
    print('Course Description: ', courseDetail[2])
    print('Start Date: ', courseDetail[3])
    print('End Date: ', courseDetail[4])
    print('Marks Obtaines: ', courseDetail[5])
    print('Certificate Issued: ', courseDetail[6])
    print('Course Teacher: ', courseDetail[8],' (', courseDetail[7], ') ')
    while True:
        print("=================================================================================")
        print('Enter 0000 to Go back')

        c_idChoice = int(input('Enter: '))

        if c_idChoice == 0000:
            return
        else:
            print('\n Enter Correct Choice.')
