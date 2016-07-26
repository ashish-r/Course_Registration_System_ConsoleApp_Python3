import sqlite3

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def create_courses_table():
    curr.execute("CREATE TABLE IF NOT EXISTS courses(c_id INTEGER, c_name TEXT, c_description TEXT, c_startdate DATE, c_enddate DATE, c_teacherid INTEGER)")

def create_course_student_table():
    curr.execute("CREATE TABLE IF NOT EXISTS course_student(c_id INTEGER, s_id INTEGER, marks INTEGER, certificate BOOLEAN DEFAULT FALSE )")

def reg_course(cid,sid):
    curr.execute("INSERT INTO course_student (c_id, s_id, certificate) VALUES(?,?,'FALSE')",(cid,sid))
    conn.commit()
    print('REGISTRATION SUCCESSFUL')



def viewAvlCourses(sid):
    curr.execute("SELECT c_id ,c_name,c_startdate from courses  where c_startdate>=date('now')")
    conn.commit()
    courses = curr.fetchall()
    print("COURSES ARE:")
    print(" ID  - NAME - Start Date")
    for course in courses:
        print(course[0], ' - ', course[1], ' - ', course[2])
    avlCourseId = [int(i[0]) for i in courses]
    print("=================================================================================")
    print('Enter Course Id For Details')
    print('Or Enter 0000 to go back')
    c_idChoice = int(input())
    if c_idChoice == 0000:
        return 
    elif c_idChoice in avlCourseId:

        print("Course Details")
        view_course_detail(c_idChoice, sid)
    else:
        print('CHOOSE CORRECT OPTION \n')


def view_course_detail(cid, sid):
    curr.execute("SELECT courses.c_id, courses.c_name, courses.c_description, courses.c_startdate, courses.c_enddate, teachers.t_id, teachers.t_name  from courses,teachers where courses.c_id=:c_id and teachers.t_id = courses.c_teacherid",{"c_id": cid})
    conn.commit()
    courseDetail = curr.fetchone()

    print('Course ID: ', courseDetail[0], ' Course Name: ', courseDetail[1])
    print('Course Description: ', courseDetail[2])
    print('Start Date: ', courseDetail[3])
    print('End Date: ', courseDetail[4])
    print('Course Teacher: ', courseDetail[6], ' (', courseDetail[5], ') ')

    curr.execute("SELECT count(*) from course_student where c_id=:c_id and s_id=:s_id",{"c_id": cid, "s_id":sid})
    conn.commit()
    data = curr.fetchone()
    count = data[0]
    if (count >= 1):
        cregchk =1
    else:
        cregchk = 0
    while True:
        if cregchk ==1:
            print('YOU ARE ENROLLED IN THIS COURSE')
            print("=================================================================================")
            print('Enter 0000 to Go back')
            c_idChoice = int(input('Enter: '))

            if c_idChoice == 0000:
                return

            else:
                print('\n Enter Correct Choice.')


        else:
            print("=================================================================================")
            print('\n \n Enter 1 to REGISTER in this course')
            print('Or Enter 0000 to Go back')
            c_idChoice = int(input('Enter: '))

            if c_idChoice == 0000:
                return
            elif c_idChoice == 1:
                reg_course(cid, sid)
                break
            else:
                print('\n Enter Correct Choice.')

