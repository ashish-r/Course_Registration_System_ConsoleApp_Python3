import sqlite3

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def view_teacher_course():
    curr.execute("select teachers.t_id, teachers.t_name, courses.c_id, courses. c_name, courses.c_startdate from courses, teachers where courses.c_teacherid = teachers.t_id")
    conn.commit()
    teacherCourses = curr.fetchall()
    print('T_ID   T_Name   C_ID   C_Name   Start Date')
    for teacherCourse in teacherCourses:
        print(teacherCourse[0], ' - ', teacherCourse[1], ' - ', teacherCourse[2], ' - ', teacherCourse[3], ' - ',teacherCourse[4] )

    while True:
        print("=================================================================================")
        bckchoice = int(input('Enter 0000 to go back: '))

        if bckchoice==0000:
            return
        else:
            print('Enter Valid Choice')
