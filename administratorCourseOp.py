import sqlite3

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()


def create_courses_table():
    curr.execute(
        "CREATE TABLE IF NOT EXISTS courses(c_id INTEGER, c_name TEXT, c_description TEXT, c_startdate DATE, c_enddate DATE, c_teacherid INTEGER)")


def course_data_entry():
    c_id = int(input("Enter Course ID: "))
    c_name = input("Course Name: ")
    c_description = input("Course Description: ")
    c_startdate = input("Start Date(yyyy-mm-dd): ")
    c_enddate = input("End Date(yyyy-mm-dd): ")
    c_teacherid = int(input("Id Of Teacher: "))
    curr.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)",
                 (c_id, c_name, c_description, c_startdate, c_enddate, c_teacherid))
    conn.commit()
    print('Data Inserted Successfully')


def viewAvlCourses():
    while True:
        curr.execute("SELECT c_id ,c_name,c_startdate FROM courses  WHERE c_startdate>=date('now')")
        conn.commit()
        courses = curr.fetchall()
        print("\nCOURSES ARE:")
        print(" ID  - NAME - Start Date")
        for course in courses:
            print(course[0], ' - ', course[1], ' - ', course[2])
        avlCourseId = [int(i[0]) for i in courses]
        print("=================================================================================")
        print('\nEnter 9999 to Also View Old Courses')
        print('Or Enter Course Id For Details')
        print('Or Enter 0000 to go back')
        c_idChoice = int(input())
        if c_idChoice == 9999:
            viewAllCourses()
        elif c_idChoice == 0000:
            return
        elif c_idChoice in avlCourseId:
            view_course_detail(c_idChoice)
        else:
            print('CHOOSE CORRECT OPTION \n')


def viewAllCourses():
    while True:
        curr.execute("SELECT c_id ,c_name,c_startdate FROM courses")
        conn.commit()
        courses = curr.fetchall()
        print("\nCOURSES ARE:")
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
            view_course_detail(c_idChoice)
        else:
            print('CHOOSE CORRECT OPTION \n')


def del_course(cid):
    curr.execute("DELETE FROM courses WHERE c_id=:c_id", {"c_id": cid})
    conn.commit()
    print('COURSE DELETED SUCCESSFULLY')
    viewAvlCourses()


def update_course(cid):
    curr.execute("SELECT * FROM courses WHERE c_id=:c_id", {"c_id": cid})
    conn.commit()
    courseDetail = curr.fetchone()

    ocid = courseDetail[0]
    ocname = courseDetail[1]
    ocdesc = courseDetail[2]
    ostrtdate = courseDetail[3]
    oenddate = courseDetail[4]
    otchr = courseDetail[5]

    print('Old Course Name: ', ocname, ' \nEnter New Course Name: ')
    ncname = input()
    if(ncname == '') :
        ncname=ocname
    print('Old Course Description: ', ocdesc, ' \nEnter New Course Description: ')
    ncdesc = input()
    if(ncdesc == ''):
        ncdesc = ocdesc
    print('Old Course Start Date: ', ostrtdate, ' \nEnter New Course Start Date: ')
    nstrtdate = input()
    if(nstrtdate == ''):
        nstrtdate = ostrtdate
    print('Old Course End Date: ', oenddate, ' \nEnter New Course End Date: ')
    nenddate = input()
    if(nenddate == ''):
        nenddate = oenddate
    print('Old Teacher Id For This Course: ', otchr, ' \nEnter New Teacher Id For This Course: ')
    temp = input()
    if temp == '' :
        ntchr = otchr
    else: ntchr = int(temp)

    curr.execute(
        "UPDATE courses SET c_name = :c_name, c_description = :c_description, c_startdate = :c_startdate,  c_enddate = :c_enddate, c_teacherid = :c_teacherid WHERE courses.c_id = :c_id",
        ({"c_name": ncname, "c_description": ncdesc, "c_startdate": nstrtdate, "c_enddate": nenddate,
          "c_teacherid": ntchr, "c_id": ocid}))
    conn.commit()

    print('COURSE UPDATED SUCCESSFULLY')
    view_course_detail(ocid)

def student_in_course(cid):
    curr.execute(
        "SELECT course_student.s_id, students.s_name from course_student,students where course_student.c_id=:c_id and course_student.s_id = students.s_id",
        {"c_id": cid})
    conn.commit()
    courseStudents = curr.fetchall()
    print('S_ID - S_Name')
    for courseStudent in courseStudents:
        print(courseStudent[0], ' ', courseStudent[1] )




def view_course_detail(cid):
    curr.execute("SELECT courses.c_id, courses.c_name, courses.c_description, courses.c_startdate, courses.c_enddate, teachers.t_id, teachers.t_name  from courses,teachers where courses.c_id=:c_id and teachers.t_id = courses.c_teacherid",{"c_id": cid})
    conn.commit()
    courseDetail = curr.fetchone()

    print('Course ID: ', courseDetail[0], ' Course Name: ', courseDetail[1])
    print('Course Description: ', courseDetail[2])
    print('Start Date: ', courseDetail[3])
    print('End Date: ', courseDetail[4])
    print('Course Teacher: ', courseDetail[6], ' (', courseDetail[5], ') ')
    while True:
        print("=================================================================================")
        print('\nEnter 1 to DELETE the course')
        print('Enter 2 to EDIT the course')
        print('Enter 3 to View Students Enrolled in this course')
        print('Or Enter 0000 to Go back')

        c_idChoice = int(input('Enter: '))

        if c_idChoice == 0000:
            return
        if c_idChoice == 1:
            del_course(courseDetail[0])
        if c_idChoice == 2:
            update_course(courseDetail[0])
        if c_idChoice == 3:
            student_in_course(courseDetail[0])
        else:
            print('\n Enter Correct Choice.')


def courseCalendar():
    while True:
        curr.execute("SELECT c_id ,c_name,c_startdate FROM courses  WHERE c_startdate>=date('now') order by c_startdate")
        conn.commit()
        courses = curr.fetchall()
        print("COURSES ARE:")
        print("Start Date - ID  - NAME")
        for course in courses:
            print(course[2],' - ',course[0], ' - ', course[1])
        avlCourseId = [int(i[0]) for i in courses]
        print("=================================================================================")
        print('Enter Course Id For Details')
        print('Or Enter 0000 to go back')
        c_idChoice = int(input())
        if c_idChoice == 0000:
            return
        elif c_idChoice in avlCourseId:
            view_course_detail(c_idChoice)
        else:
            print('CHOOSE CORRECT OPTION \n')


def main():


    while True:
        print("=================================================================================")
        print('Enter 1 to add a course')
        print('Enter 2 to view all courses')
        print('Enter 0000 to Go back')

        choice = int(input('Enter: '))

        if choice == 1:
            create_courses_table()
            try:
                course_data_entry()
            except:
                print('Data  entry failed. Please Try Again.')
                course_data_entry()

        elif choice == 2:
            viewAvlCourses()
        elif choice == 0000:
            return 

        else:
            print('PLEASE ENTER A VALID CHOICE \n')