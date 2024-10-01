from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from TeacherApp.models import Teacher, Course_Instructor
from StudentApp.models import Student, Semester
from ResultApp.models import Course_Mark, Semester_Result  # Import Semester_Result
from django.views.decorators.cache import never_cache

# Grading System (Corresponding GPA for each percentage)
def calculate_grade_point(total_marks):
    if total_marks >= 80:
        return 4.00
    elif total_marks >= 75:
        return 3.75
    elif total_marks >= 70:
        return 3.50
    elif total_marks >= 65:
        return 3.25
    elif total_marks >= 60:
        return 3.00
    elif total_marks >= 55:
        return 2.75
    elif total_marks >= 50:
        return 2.50
    elif total_marks >= 45:
        return 2.25
    elif total_marks >= 40:
        return 2.00
    else:
        return 0.00

# Teacher Login View
@never_cache  # Prevents caching of the login page
def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('TeacherApp:teacher_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Teacher.objects.filter(user=user).exists():
                login(request, user)
                return redirect('TeacherApp:teacher_dashboard')
            else:
                messages.error(request, 'You do not have permission to log in as a teacher.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'teacher_app/teacher_login.html')


# Teacher Logout View
@login_required(login_url='TeacherApp:teacher_login')
def teacher_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')

    response = redirect('TeacherApp:teacher_login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


# Teacher Dashboard View
@login_required(login_url='TeacherApp:teacher_login')
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        assigned_courses = Course_Instructor.objects.filter(teacher_id=teacher)

        return render(request, 'teacher_app/teacher_dashboard.html', {
            'teacher': teacher,
            'assigned_courses': assigned_courses
        })
    except Teacher.DoesNotExist:
        messages.error(request, 'You do not have a teacher profile.')
        return redirect('TeacherApp:teacher_login')


@login_required(login_url='TeacherApp:teacher_login')
def enter_marks(request, course_code):
    try:
        teacher = Teacher.objects.get(user=request.user)
        course_instructor = get_object_or_404(Course_Instructor, courseinfo__course_code=course_code, teacher_id=teacher)
        students = Student.objects.filter(curr_semester=course_instructor.courseinfo.semester)
        student_marks = {}

        if request.method == 'POST':
            for student in students:
                attendance = float(request.POST.get(f'attendance_{student.id}', 0))  # Convert to float
                assignment = float(request.POST.get(f'assignment_{student.id}', 0))  # Convert to float
                mid_exam = float(request.POST.get(f'mid_exam_{student.id}', 0))  # Convert to float
                final_exam = float(request.POST.get(f'final_exam_{student.id}', 0))  # Convert to float

                total_marks = attendance + assignment + mid_exam + final_exam

                # Create or update the marks for each student
                Course_Mark.objects.update_or_create(
                    course_id=course_instructor.courseinfo,
                    student_id=student,
                    defaults={
                        'attendance': attendance,
                        'assignment': assignment,
                        'mid_exam': mid_exam,
                        'final_exam': final_exam,
                        'total': total_marks
                    }
                )

                # Calculate GPA for the course
                grade_point = calculate_grade_point(total_marks)
                course_credit = float(course_instructor.courseinfo.credit_hour)  # Convert to float
                student_gpa = grade_point * course_credit

                # Update Semester GPA
                update_semester_gpa(student, course_credit, student_gpa)

            messages.success(request, 'Marks have been successfully entered.')
            return redirect('TeacherApp:teacher_dashboard')

        # Fetch marks for each student
        for student in students:
            course_mark = Course_Mark.objects.filter(course_id=course_instructor.courseinfo, student_id=student).first()
            student_marks[student.id] = {
                'attendance': float(course_mark.attendance) if course_mark else 0.0,
                'assignment': float(course_mark.assignment) if course_mark else 0.0,
                'mid_exam': float(course_mark.mid_exam) if course_mark else 0.0,
                'final_exam': float(course_mark.final_exam) if course_mark else 0.0,
                'total': float(course_mark.total) if course_mark else 0.0
            }

        return render(request, 'teacher_app/enter_marks.html', {
            'course_instructor': course_instructor,
            'students': students,
            'student_marks': student_marks
        })

    except Teacher.DoesNotExist:
        messages.error(request, 'You do not have access to enter marks for this course.')
        return redirect('TeacherApp:teacher_dashboard')


def update_semester_gpa(student, course_credit, student_gpa):
    course_marks = Course_Mark.objects.filter(student_id=student, course_id__semester=student.curr_semester)

    total_grade_points = 0.0  # Use float for consistency
    total_credits = 0.0  # Use float for consistency

    for mark in course_marks:
        total_grade_points += float(calculate_grade_point(mark.total)) * float(mark.course_id.credit_hour)  # Convert to float
        total_credits += float(mark.course_id.credit_hour)  # Convert to float

    gpa = total_grade_points / total_credits if total_credits > 0 else 0.0  # Ensure GPA is a float

    Semester_Result.objects.update_or_create(
        student_id=student,
        semester=student.curr_semester,
        defaults={'gpa': gpa}
    )

    update_cgpa(student)



def update_cgpa(student):
    semester_results = Semester_Result.objects.filter(student_id=student)

    total_gpa = 0.0  # Use float for consistency
    total_credits = 0.0  # Use float for consistency

    for result in semester_results:
        courses = Course_Mark.objects.filter(student_id=student, course_id__semester=result.semester)
        for course in courses:
            total_gpa += float(result.gpa) * float(course.course_id.credit_hour)  # Convert to float
            total_credits += float(course.course_id.credit_hour)  # Convert to float

    cgpa = total_gpa / total_credits if total_credits > 0 else 0.0  # Ensure CGPA is a float

    student.cgpa = cgpa
    student.save()

    check_promotion(student)



def check_promotion(student):
    semester_result = Semester_Result.objects.get(student_id=student, semester=student.curr_semester)

    if semester_result.gpa >= 2.000 and student.cgpa >= 2.250 and not has_failing_grade(student):
        next_semester = Semester.objects.get(semester_number=student.curr_semester.semester_number + 1)
        student.curr_semester = next_semester
        student.save()


def has_failing_grade(student):
    failing_courses = Course_Mark.objects.filter(student_id=student).filter(total__lt=40)
    return failing_courses.exists()
