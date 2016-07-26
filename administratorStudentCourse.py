import sqlite3

conn = sqlite3.connect('OpenOnlineCourse.db')
curr = conn.cursor()


def course_student_data_entry():
    curr.execute(
        "CREATE TABLE IF NOT EXISTS course_student(c_id INTEGER, s_id INTEGER, marks INTEGER, certificate BOOLEAN DEFAULT FALSE )")
    c_id = int(input("Enter Course Id: "))
    s_id = int(input("Enter Student Id: "))
    marks = int(input("Enter Marks: "))
    certificate = input("Certificate: ")
    try:
        curr.execute("INSERT INTO course_student VALUES(?,?,?,?)", (c_id, s_id, marks, certificate))
        conn.commit()
    except:
        print('Data  entry failed. Please Try Again.')
        conn.commit()
        return
    print('Data Inserted Successfully')


def view_all():
    curr.execute("SELECT course_student.c_id,course_student.s_id, courses.c_name, courses.c_startdate, students.s_name FROM course_student, courses, students where course_student.c_id=courses.c_id and course_student.s_id = students.s_id")
    conn.commit()
    details = curr.fetchall()
    print("STUDENT COURSE DETAILS:")
    print("Student ID - Student Name -  Course ID - Course Name - Course Start Date")
    for detail in details:
        print(detail[1], ' - ', detail[4], ' - ',detail[0], ' - ',detail[2], ' - ',detail[3])

    avlcid = [int(i[0]) for i in details]
    avlsid = [int(i[1]) for i in details]
    print('\n \nEnter Course Id and Student Id For Details')
    print('Or Enter 0000 to go back')
    t_idChoice1 = int(input('Enter Course Id'))
    t_idChoice2 = int(input('Enter Student Id'))
    if t_idChoice1 == 0000 or t_idChoice2 == 0000:
        return
    elif t_idChoice1 in avlcid and t_idChoice2 in avlsid:
        view_one(t_idChoice1, t_idChoice2)
    else:
        print('CHOOSE CORRECT OPTION \n')
        view_all()


def del_record(cid, sid):
    try:
        curr.execute("DELETE FROM course_student WHERE c_id=:c_id AND s_id=:s_id", {"c_id": cid, "s_id": sid})
        conn.commit()
    except:
        print("Something went wrong there. Try again")
        conn.commit()
        return
    print('Teacher DELETED SUCCESSFULLY')
    view_all()


def update_record(cid, sid):
    curr.execute("SELECT * FROM course_student WHERE c_id=:c_id AND s_id=:s_id", {"c_id": cid, "s_id": sid})
    conn.commit()
    Detail = curr.fetchone()

    old_cid = Detail[0]
    old_sid = Detail[1]
    old_marks = Detail[2]
    oid_certificate = Detail[3]

    print('Old Course Id : ', old_cid, ' \nEnter New Course Id: ')
    new_cid = input()
    print('Old Student Id: ', old_sid, ' \nEnter New Student Id: ')
    new_sid = input()
    print('Old Marks: ', old_marks, ' \nEnter New Marks: ')
    new_marks = input()
    print('Old certificate Value: ', oid_certificate, ' \nEnter certificate Value: ')
    new_certificate = input()

    curr.execute(
        "UPDATE course_student SET c_id = :c_id, s_id = :s_id, marks = :marks,  certificate = :certificate WHERE c_id=:cid AND s_id=:sid",
        (
        {"c_id": new_cid, "s_id": new_sid, "marks": new_marks, "certificate": new_certificate, "cid": cid, "sid": sid}))
    conn.commit()

    print('Teacher UPDATED SUCCESSFULLY')
    view_one(new_cid, new_sid)


def view_one(cid, sid):
    curr.execute("SELECT course_student.c_id,course_student.s_id, courses.c_name, courses.c_startdate, students.s_name, course_student.certificate,course_student.marks FROM course_student, courses, students where course_student.c_id=courses.c_id and course_student.s_id = students.s_id and course_student.c_id=:c_id and course_student.s_id =:s_id", {"c_id": cid, "s_id": sid})
    conn.commit()
    Detail = curr.fetchone()

    print('Cource ID: ', Detail[0])
    print('Cource Name: ', Detail[2])
    print('Student ID: ', Detail[1])
    print('Student Name: ', Detail[4])
    print('Course Start Date: ', Detail[3])
    print('Marks: ', Detail[6])
    print('Certificate: ', Detail[5])
    while True:
        print("=================================================================================")
        print('\n \n Enter 1 to DELETE the record')
        print('Enter 2 to EDIT the record')
        print('Or Enter 0000 to Go back')

        t_idChoice = int(input('Enter: '))

        if t_idChoice == 0000:
            return
        if t_idChoice == 1:
            del_record(Detail[0], Detail[1])
        if t_idChoice == 2:
            update_record(Detail[0], Detail[1])
        else:
            print('\n Enter Correct Choice.')


def main():


    while True:
        print("=================================================================================")
        print('Enter 1 to enroll a student in a course')
        print('Enter 2 to view all student-course Records')
        print('Enter 0000 to return')

        choice = int(input('Enter: '))

        if choice == 1:
            course_student_data_entry()

        elif choice == 2:
            view_all()
        elif choice == 0000:
            return

        else:
            print('PLEASE ENTER A VALID CHOICE \n')
