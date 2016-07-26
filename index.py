import sqlite3
import studentMaster
import administratorMaster
conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def create_students_table():
    curr.execute("CREATE TABLE IF NOT EXISTS students(s_id INTEGER PRIMARY KEY, s_name TEXT, s_gender TEXT, s_email TEXT, s_phone INTEGER, s_dateEnrolled DATE)")

def create_student_login_table():
    curr.execute("CREATE TABLE IF NOT EXISTS student_login(s_email TEXT, s_pwd TEXT)")

while True:
    try:
        create_students_table()
        create_student_login_table()
        while True:
            print("=================================================================================")
            try:
                loginChoice = int(input('Enter 1 to login as Administrator \n2 to login / register as student: '))
            except:
                print('Wrong Choice. Please Try Again.')

            if loginChoice == 1:
                while True:
                    try:
                        admkey = int(input('Enter administrator key: '))
                    except:
                        print('Administrator Key is wrong. Please Try Again. \n')
                    if admkey == 1201:
                        print('=====Admin Panel=====')
                        administratorMaster.main()
                        break
                    else:
                        print('Administrator Key is wrong. Please Try Again. \n')

            elif loginChoice == 2:
                print("=================================================================================")
                print('=======STUDENT SECTION========')
                while True:
                    print("=================================================================================")
                    try:
                        slchoice = int(input('Enter 1 to Login \n2 to register\n Enter:'))
                    except:
                        print('Wrong Choice. Please Try Again.')
                    if slchoice == 1:
                        print('=======STUDENT LOGIN======')
                        studentMaster.student_login()

                    elif slchoice == 2:
                        print('======STUDENT REGISTRATION======')
                        studentMaster.student_registration()
                    else:
                        print('Wrong Choice. Please Try Again.')

            else:
                print('Wrong Choice. Please Try Again.')


    except:
        print('Invalid Choice.')