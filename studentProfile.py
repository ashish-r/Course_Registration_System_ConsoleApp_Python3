import sqlite3
import re
conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()

def create_students_table():
    curr.execute("CREATE TABLE IF NOT EXISTS students(s_id INTEGER PRIMARY KEY, s_name TEXT, s_gender TEXT, s_email TEXT, s_phone INTEGER, s_dateEnrolled DATE)")

def update_profile(sid):
    curr.execute("SELECT * from students where s_id=:s_id", {"s_id": sid})
    conn.commit()
    studentDetail = curr.fetchone()

    osid = studentDetail[0]
    osname = studentDetail[1]
    osgender = studentDetail[2]
    osemail = studentDetail[3]
    osphone = studentDetail[4]
    nsname = ''
    nsgender = ''
    nsemail = ''
    nsphone = 0
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

    curr.execute(
        "UPDATE students set s_name = :s_name, s_gender = :s_gender, s_email = :s_email,  s_phone = :s_phone where students.s_id = :s_id",
        ({"s_name": nsname, "s_gender": nsgender, "s_email": nsemail, "s_phone": nsphone, "s_id": osid}))
    conn.commit()

    print('Profile UPDATED SUCCESSFULLY')
    view_profile(osid)


def view_profile(sid):
    curr.execute("SELECT * from students where s_id=:s_id", {"s_id": sid})
    conn.commit()
    studentDetail = curr.fetchone()
    print('\nWelcome', studentDetail[1])
    print('\nID: ', studentDetail[0], )
    print('Gender: ', studentDetail[2])
    print('Email: ', studentDetail[3])
    print('Phone: ', studentDetail[4])
    print('Date Of Enrollment: ', studentDetail[5])
    while True:
        print("=================================================================================")
        print('\nEnter 1 to EDIT your details')
        print('Or Enter 0000 to Go back')

        s_idChoice = int(input('Enter: '))

        if s_idChoice == 0000:
            return
        elif s_idChoice == 1:
            update_profile(studentDetail[0])
        else:
            print('\n Enter Correct Choice.')

