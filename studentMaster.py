import sqlite3
import studentCourseReg
import studentCourseSelect
import studentProfile
import re

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def create_students_table():
    curr.execute("CREATE TABLE IF NOT EXISTS students(s_id INTEGER PRIMARY KEY, s_name TEXT, s_gender TEXT, s_email TEXT, s_phone INTEGER, s_dateEnrolled DATE)")

def create_student_login_table():
    curr.execute("CREATE TABLE IF NOT EXISTS student_login(s_email TEXT, s_pwd TEXT)")

def student_registration():
    # validation required
    s_name = ''
    s_gender = ''
    s_email = ''
    s_phone = 0
    s_dateEnrolled = ''
    while not s_name.isalpha():
        s_name = input("Enter Student Name: ")
        if not s_name.isalpha():
            print("invalid name")

    while not s_gender.lower() == 'male' or s_gender.lower() == 'female':
        s_gender = input("Enter Gender: ")
        if not s_gender.lower() == 'male' or s_gender.lower() == 'female':
            print("invalid input")

    while not re.search('\S+@\S+.com', s_email):
        s_email = input("Email: ")
        if not re.search('\S+@\S+.com', s_email):
            print("invalid input")

    while len(str(s_phone)) != 10:
        s_phone = int(input("Phone: "))
        if len(str(s_phone)) != 10:
            print("invalid input")

    s_pwd = input("Enter Password: ")
    create_students_table()
    create_student_login_table()
    curr.execute(
        "INSERT INTO students (s_name, s_gender, s_email, s_phone, s_dateEnrolled) VALUES(?,?,?,?,date('now'))",
        (s_name, s_gender, s_email, s_phone))
    conn.commit()
    curr.execute("INSERT INTO student_login  VALUES(?,?)", (s_email, s_pwd))
    conn.commit()
    print('Registration Successfully')



def student_login():


    while True:
        semail = input("Enter Your Email Id or 0000 to exit")
        if semail == '0000':
            return
        spassword = input("Enter Your Password")
        curr.execute(
            "SELECT count(*) FROM student_login WHERE student_login.s_email = ? AND student_login.s_pwd = ?",
            (semail, spassword))
        data = curr.fetchone()
        count = data[0]
        if (count >= 1):
            print("Login Successful")
            curr.execute("SELECT s_id, s_name FROM students WHERE students.s_email=:s_email", {"s_email": semail})
            conn.commit()
            student = curr.fetchone()
            sid = student[0]
            print('\nWELCOME ', student[1])
            while True:
                print("=================================================================================")
                print("Enter 1 to Display/Edit Profile")
                print("Enter 2 to Display Registered Courses")
                print("Enter 3 to Display All Available Courses")
                print("Enter 0000 to return")

                schoiceh = int(input('Enter: '))
                if schoiceh == 1:
                    print("======Profile======")
                    studentProfile.view_profile(sid)
                elif schoiceh == 2:
                    print("======Registered Courses=======")
                    studentCourseReg.view_registered_courses(sid)

                elif schoiceh == 3:
                    print("======Available Courses======")
                    studentCourseSelect.viewAvlCourses(sid)
                elif schoiceh == 0000:
                    return

                else:
                    print('Please Choose Correct Option')



        else:
            print('user Id Or Password Incorrect')
