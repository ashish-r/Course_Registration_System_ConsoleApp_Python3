import administratorCourseOp
import administartorTeacher
import administratorStudent
import administratorStudentCourse
import administratorTeacherCourse
def choice_administrator_home():
    print("=================================================================================")
    print('Enter 1 to manage courses')
    print('Enter 2 to manage teachers')
    print('Enter 3 to manage students')
    print('Enter 4 to manage student-course')
    print('Enter 5 to view teacher-course')
    print('Enter 6 to view course-calendar')
    print('Enter 0000 to logout')
    print('Enter: ')


def main():
   while True:
        choice_administrator_home()
        choice = int(input())

        if choice == 1:
            print('======MANAGE  COURSES=====')
            administratorCourseOp.main()
        elif choice == 2:
            print('=====MANAGE  TEACHERS=====')
            administartorTeacher.main()
        elif choice == 3:
            print('=====MANAGE  STUDENT======')
            administratorStudent.main()
        elif choice == 4:
            print('======STUDENT COURSE DETAILS======')
            administratorStudentCourse.main()
        elif choice == 5:
            print('======TEACHER COURSE DETAILS======')
            administratorTeacherCourse.view_teacher_course()

        elif choice == 6:
            print('======COURSE CALENDAR=======')
            administratorCourseOp.courseCalendar()
        elif choice == 0000:
           return
        else:
            print('Please Choose Correct Option \n')
