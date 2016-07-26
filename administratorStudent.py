import sqlite3
import re

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()


def create_students_table():
    curr.execute(
        "CREATE TABLE IF NOT EXISTS students(s_id INTEGER, s_name TEXT, s_gender TEXT, s_email TEXT, s_phone INTEGER, s_dateEnrolled DATE)")


def create_student_login_table():
    curr.execute("CREATE TABLE IF NOT EXISTS student_login(s_email TEXT, s_pwd TEXT)")


def student_data_entry():
    s_name = ''
    s_gender = ''
    s_email = ''
    s_phone = 0
    s_dateEnrolled = ''
    s_id = int(input("Enter Student ID: "))
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
    while not re.search('....[-]..[-]..', s_dateEnrolled):
        s_dateEnrolled = input("Date Of Enrollment (yyyy-mm-dd) ")
        if not re.search('....[-]..[-]..', s_dateEnrolled):
            print('Invalid Date')
    curr.execute("INSERT INTO students VALUES(?,?,?,?,?,?)", (s_id, s_name, s_gender, s_email, s_phone, s_dateEnrolled))
    conn.commit()
    curr.execute("INSERT INTO student_login  VALUES(?,?)", (s_email, s_phone))
    conn.commit()
    print('Data Inserted Successfully')


def viewAllStudents():
    curr.execute("SELECT s_id ,s_name,s_email FROM students")
    conn.commit()
    students = curr.fetchall()
    print("\nStudents ARE:")
    print(" ID  - NAME - Email")
    for student in students:
        print(student[0], ' - ', student[1], ' - ', student[2])
    avlStudentId = [int(i[0]) for i in students]
    print('\n \nEnter Student Id For Details')
    print('Or Enter 0000 to go back')
    s_idChoice = int(input())
    if s_idChoice == 0000:
        return
    elif s_idChoice in avlStudentId:
        view_student_detail(s_idChoice)
    else:
        print('CHOOSE CORRECT OPTION \n')
        viewAllStudents()


def del_student(sid):
    curr.execute("DELETE FROM students WHERE s_id=:s_id", {"s_id": sid})
    conn.commit()
    print('Student DELETED SUCCESSFULLY')
    viewAllStudents()


def update_student(sid):
    curr.execute("SELECT * FROM students WHERE s_id=:s_id", {"s_id": sid})
    conn.commit()
    studentDetail = curr.fetchone()

    osid = studentDetail[0]
    osname = studentDetail[1]
    osgender = studentDetail[2]
    osemail = studentDetail[3]
    osphone = studentDetail[4]
    osdateEnrolled = studentDetail[5]

    nsname = ''
    nsgender = ''
    nsemail = ''
    nsphone = 0
    nsdateEnrolled = ''
    print('Old Student Name: ', osname, ' \nEnter New Student Name: ')
    while not nsname.isalpha():
        nsname = input()
        if nsname == '':
            nsname = osname
        if not nsname.isalpha():
            print("invalid input")
    print('Old Student Gender: ', osgender, ' \nEnter New Student Gender: ')
    while not nsgender.lower() == 'male' or nsgender.lower() == 'female':
        nsgender = input()
        if nsgender == '':
            nsgender = osgender
        if not nsgender.lower() == 'male' or nsgender.lower() == 'female':
            print("invalid input")
    print('Old Email: ', osemail, ' \nEnter New Email: ')
    while not re.search('\S+@\S+.com', nsemail):
        nsemail = input()
        if nsemail == '':
            nsemail = osemail
        if not re.search('\S+@\S+.com', nsemail):
            print("invalid input")

    print('Old Phone: ', osphone, ' \nEnter New Phone: ')
    while len(str(nsphone)) != 10:
        nsphone = input()
        if nsphone == '':
            nsphone = osphone
        else:
            nsphone = int(nsphone)
        if len(str(nsphone)) != 10:
            print("invalid input")

    print('Old Student Date Enrolled: ', osdateEnrolled, ' \nEnter New Student Date Enrolled: ')
    while not re.search('....[-]..[-]..', nsdateEnrolled):
        nsdateEnrolled = input()
        if nsdateEnrolled == '':
            nsdateEnrolled = osdateEnrolled
        if not re.search('....[-]..[-]..', nsdateEnrolled):
            print('Invalid Date')

    curr.execute(
        "UPDATE students SET s_name = :s_name, s_gender = :s_gender, s_email = :s_email,  s_phone = :s_phone, s_dateEnrolled = :s_dateEnrolled WHERE students.s_id = :s_id",
        ({"s_name": nsname, "s_gender": nsgender, "s_email": nsemail, "s_phone": nsphone,
          "s_dateEnrolled": nsdateEnrolled, "s_id": osid}))
    conn.commit()

    print('Student UPDATED SUCCESSFULLY')
    view_student_detail(osid)

def courses_student(sid):
    curr.execute("SELECT course_student.c_id, courses.c_name, courses.c_startdate from course_student,courses where course_student.s_id=:s_id and course_student.c_id = courses.c_id", {"s_id": sid})
    conn.commit()
    studentDetails = curr.fetchall()
    print('C_ID  C_NAME  START DATE')
    for studentDetail in studentDetails:
        print(studentDetail[0], ' ', studentDetail[1], ' ', studentDetail[2])


def view_student_detail(sid):
    curr.execute("SELECT * FROM students WHERE s_id=:s_id", {"s_id": sid})
    conn.commit()
    studentDetail = curr.fetchone()

    print('Student ID: ', studentDetail[0], '\nStudent Name: ', studentDetail[1])
    print('Student Gender: ', studentDetail[2])
    print('Email: ', studentDetail[3])
    print('Phone: ', studentDetail[4])
    print('Date Of Enrollment: ', studentDetail[5])
    while True:
        print("=================================================================================")
        print('\n \n Enter 1 to DELETE the student')
        print('Enter 2 to EDIT the student details')
        print('Enter 3 to VIEW all the courses of this student')
        print('Or Enter 0000 to Go back')

        s_idChoice = int(input('Enter: '))

        if s_idChoice == 0000:
            return
        if s_idChoice == 1:
            del_student(studentDetail[0]
                        )
        if s_idChoice == 2:
            update_student(studentDetail[0])

        if s_idChoice == 3:
            courses_student(studentDetail[0])
        else:
            print('\n Enter Correct Choice.')


def main():
    create_student_login_table()
    create_students_table()
    while True:
        print("=================================================================================")
        print('Enter 1 to add a Student')
        print('Enter 2 to view all Students')
        print('Enter 0000 to Go back')

        choice = int(input('Enter: '))

        if choice == 1:
            try:
                student_data_entry()
            except:
                print('Data  entry failed. Please Try Again.')
                student_data_entry()

        elif choice == 2:
            viewAllStudents()

        elif choice == 0000:
            return

        else:
            print('PLEASE ENTER A VALID CHOICE \n')
