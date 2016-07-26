import sqlite3
import re

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()


def create_teachers_table():
    curr.execute(
        "CREATE TABLE IF NOT EXISTS teachers(t_id INTEGER, t_name TEXT, t_gender TEXT, t_email TEXT, t_phone INTEGER, t_dept TEXT)")


def teacher_data_entry():
    t_name = ''
    t_gender = ''
    t_email = ''
    t_phone = 0
    t_dept = ''
    t_id = int(input("Enter Teacher ID: "))
    while not t_name.isalpha():
        t_name = input("Enter Teacher Name: ")
        if not t_name.isalpha():
            print("invalid name")

    while not t_gender.lower() == 'male' or t_gender.lower() == 'female':
        t_gender = input("Enter Gender: ")
        if not t_gender.lower() == 'male' or t_gender.lower() == 'female':
            print("invalid input")

    while not re.search('\S+@\S+.com', t_email):
        t_email = input("Email: ")
        if not re.search('\S+@\S+.com', t_email):
            print("invalid input")

    while len(str(t_phone)) != 10:
        t_phone = int(input("Phone: "))
        if len(str(t_phone)) != 10:
            print("invalid input")
    while not t_dept.isalpha():
        t_dept = input("Department Of Teacher: ")
        if not t_dept.isalpha():
            print("invalid input")

    curr.execute("INSERT INTO teachers VALUES(?,?,?,?,?,?)", (t_id, t_name, t_gender, t_email, t_phone, t_dept))
    conn.commit()
    print('Data Inserted Successfully')


def viewAllTeachers():
    curr.execute("SELECT t_id ,t_name,t_dept FROM teachers")
    conn.commit()
    teachers = curr.fetchall()
    print("Teachers ARE:")
    print(" ID  - NAME - DPT")
    for teacher in teachers:
        print(teacher[0], ' - ', teacher[1], ' - ', teacher[2])
    avlTeacherId = [int(i[0]) for i in teachers]
    print('\n \nEnter Teacher Id For Details')
    print('Or Enter 0000 to go back')
    t_idChoice = int(input())
    if t_idChoice == 0000:
        return
    elif t_idChoice in avlTeacherId:
        view_teacher_detail(t_idChoice)
    else:
        print('CHOOSE CORRECT OPTION \n')
        viewAllTeachers()


def del_teacher(tid):
    curr.execute("DELETE FROM teachers WHERE t_id=:t_id", {"t_id": tid})
    conn.commit()
    print('Teacher DELETED SUCCESSFULLY')
    viewAllTeachers()


def update_teacher(tid):
    curr.execute("SELECT * FROM teachers WHERE t_id=:t_id", {"t_id": tid})
    conn.commit()
    teacherDetail = curr.fetchone()

    otid = teacherDetail[0]
    otname = teacherDetail[1]
    otgender = teacherDetail[2]
    otemail = teacherDetail[3]
    otphone = teacherDetail[4]
    otdept = teacherDetail[5]
    ntname = ''
    ntgender = ''
    ntemail = ''
    ntphone = 0
    ntdept = ''
    print('Old Teacher Name: ', otname, ' \nEnter New Teacher Name: ')
    while not ntname.isalpha():
        ntname = input()
        if ntname == '':
            ntname = otname
        if not ntname.isalpha():
            print("invalid input")
    print('Old Teacher Gender: ', otgender, ' \nEnter New Teacher Gender: ')
    while not ntgender.lower() == 'male' or ntgender.lower() == 'female':
        ntgender = input()
        if ntgender == '':
            ntgender = otgender
        if not ntgender.lower() == 'male' or ntgender.lower() == 'female':
            print("invalid input")
    print('Old Email: ', otemail, ' \nEnter New Email: ')
    while not re.search('\S+@\S+.com', ntemail):
        ntemail = input()
        if ntemail == '':
            ntemail = otemail
        if not re.search('\S+@\S+.com', ntemail):
            print("invalid input")

    print('Old Phone: ', otphone, ' \nEnter New Phone: ')
    while len(str(ntphone)) != 10:
        ntphone = input()
        if ntphone == '':
            ntphone = otphone
        else:
            ntphone = int(ntphone)
        if len(str(ntphone)) != 10:
            print("invalid input")

    print('Old Department: ', otdept, ' \nEnter New Department: ')
    while not ntdept.isalpha():
        ntdept = input()
        if ntdept == '':
            ntdept = otdept
        if not ntdept.isalpha():
            print("invalid input")

    curr.execute(
        "UPDATE teachers SET t_name = :t_name, t_gender = :t_gender, t_email = :t_email,  t_phone = :t_phone, t_dept = :t_dept WHERE teachers.t_id = :t_id",
        ({"t_name": ntname, "t_gender": ntgender, "t_email": ntemail, "t_phone": ntphone, "t_dept": ntdept,
          "t_id": otid}))
    conn.commit()

    print('Teacher UPDATED SUCCESSFULLY')
    view_teacher_detail(otid)

def teacher_course_detail(tid):
    curr.execute("select courses.c_id, courses. c_name, courses.c_startdate from courses, teachers where courses.c_teacherid = teachers.t_id and teachers.t_id=:t_id",{"t_id":tid})
    conn.commit()
    teacherCourses = curr.fetchall()
    print('C_ID  C_Name  Start Date')
    for teacherCourse in teacherCourses:
        print(teacherCourse[0],' - ',teacherCourse[1],' - ',teacherCourse[2])


def view_teacher_detail(tid):
    curr.execute("SELECT * FROM teachers WHERE t_id=:t_id", {"t_id": tid})
    conn.commit()
    teacherDetail = curr.fetchone()

    print('Teacher ID: ', teacherDetail[0], '\nTeacher Name: ', teacherDetail[1])
    print('Teacher Gender: ', teacherDetail[2])
    print('Email: ', teacherDetail[3])
    print('Phone: ', teacherDetail[4])
    print('Department: ', teacherDetail[5])
    while True:
        print("=================================================================================")
        print('\n \n Enter 1 to DELETE the teacher')
        print('Enter 2 to EDIT the teacher')
        print('Enter 3 to View Courses By this teacher')
        print('Or Enter 0000 to Go back')

        t_idChoice = int(input('Enter: '))

        if t_idChoice == 0000:
            return
        if t_idChoice == 1:
            del_teacher(teacherDetail[0]
                        )
        if t_idChoice == 2:
            update_teacher(teacherDetail[0])
        if t_idChoice == 3:
            teacher_course_detail(teacherDetail[0])
        else:
            print('\n Enter Correct Choice.')


def main():


    while True:
        print("=================================================================================")
        print('Enter 1 to add a Teacher')
        print('Enter 2 to view all Teachers')
        print('Enter 0000 to Go back')

        choice = int(input('Enter: '))

        if choice == 1:
            create_teachers_table()
            try:
                teacher_data_entry()
            except:
                print('Data  entry failed. Please Try Again.')
                teacher_data_entry()

        elif choice == 2:
            viewAllTeachers()
        elif choice == 0000:
            return 

        else:
            print('PLEASE ENTER A VALID CHOICE \n')

