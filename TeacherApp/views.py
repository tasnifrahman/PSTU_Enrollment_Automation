<<<<<<< HEAD
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
    
=======
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages

from TeacherApp.models import Teacher, Course_Instructor
from ResultApp.models import Course_Mark
from StudentApp.models import Student
from FacultyApp.models import Course

# Create your views here.
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def teacher_login(request):
    if request.user.is_authenticated:
        if Teacher.objects.filter(user=request.user).exists():
            return redirect('TeacherApp:teacher_dashboard')
        else:
            messages.error(request, 'You do not have the required permissions to access this page.')
            return redirect('FacultyApp:index')

>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

<<<<<<< HEAD
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
=======
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                teacher = Teacher.objects.get(user=user)
                login(request, user)
                return redirect('TeacherApp:teacher_dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, 'You do not have the required permissions to log in.')
        else:
            messages.error(request, 'Invalid username or password')

    # Add cache control headers to prevent caching of the login page
    response = render(request, 'teacher_login.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'  # HTTP 1.0
    response['Expires'] = '0'  # Proxies

    return response


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacher_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')  # Optional success message

    # Clear Cache on Logout
    response = redirect('TeacherApp:teacher_login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
    response['Pragma'] = 'no-cache'  # HTTP 1.0
    response['Expires'] = '0'  # Proxies
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a

    return response


<<<<<<< HEAD
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
=======
@login_required(login_url='TeacherApp:teacher_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacher_dashboard(request):
    # Create response object with the rendered template
    response = render(request, 'teacher_dashboard.html', {'user': request.user})
    
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'  # HTTP 1.0
    response['Expires'] = '0'  # Proxies
    
    return response


@login_required(login_url='TeacherApp:teacher_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myCourses(request):
    teacher = request.user.teacher  # Assuming the user has a one-to-one relation with Teacher
    assigned_courses = Course_Instructor.objects.filter(teacher_id=teacher).select_related('courseinfo')

    context = {
        'assigned_courses': assigned_courses,
        'teacher_name': teacher.user.get_full_name(),
    }

    # Add cache control headers to prevent caching
    response = render(request, 'myCourses.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'  # HTTP 1.0 backward compatibility
    response['Expires'] = '0'  # Proxies

    return response


@login_required(login_url='TeacherApp:teacher_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def enter_marks(request, course_code):
    try:
        teacher = Teacher.objects.get(user=request.user)
        course = Course.objects.get(course_code=course_code)

        # Ensure the teacher is assigned to this course
        if not Course_Instructor.objects.filter(teacher_id=teacher, courseinfo=course).exists():
            messages.error(request, "You are not assigned to this course.")
            return redirect('TeacherApp:myCourses')

        # Get all students enrolled in this course and same faculty
        students = Student.objects.filter(faculty=teacher.faculty, curr_semester=course.semester).order_by('student_id')

        # Fetch existing marks for the course and students
        existing_marks = {
            mark.student_id.id: {
                'attendance': mark.attendance,
                'assignment': mark.assignment,
                'mid_exam': mark.mid_exam,
                'final_exam': mark.final_exam,
                'total': mark.total
            }
            for mark in Course_Mark.objects.filter(course_id=course, student_id__in=students)
        }

        # Ensure existing_marks is not None and default to an empty dict
        existing_marks = existing_marks if existing_marks else {}

        if request.method == 'POST':
            # Process the marks entry form
            for student in students:
                attendance = float(request.POST.get(f'attendance_{student.id}', 0))
                assignment = float(request.POST.get(f'assignment_{student.id}', 0))
                mid_exam = float(request.POST.get(f'mid_exam_{student.id}', 0))
                final_exam = float(request.POST.get(f'final_exam_{student.id}', 0))

                # Server-side validation
                if attendance > 10 or assignment > 5 or mid_exam > 15 or final_exam > 70:
                    messages.error(request, f"Invalid marks for {student.student_id}: "
                                            f"Attendance must be <= 10, Assignment <= 5, "
                                            f"Mid Exam <= 15, Final Exam <= 70.")
                    return redirect('TeacherApp:enter_marks', course_code=course_code)

                total = attendance + assignment + mid_exam + final_exam

                # Create or update the student's marks
                Course_Mark.objects.update_or_create(
                    student_id=student,
                    course_id=course,
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
                    defaults={
                        'attendance': attendance,
                        'assignment': assignment,
                        'mid_exam': mid_exam,
                        'final_exam': final_exam,
<<<<<<< HEAD
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
=======
                        'total': total
                    }
                )

            messages.success(request, "Marks entered successfully!")
            return redirect('TeacherApp:enter_marks', course_code=course_code)

        context = {
            'course': course,
            'students': students,
            'existing_marks': existing_marks,  # Always pass a dictionary to avoid None errors
        }
        response = render(request, 'enter_marks.html', context)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

    except Teacher.DoesNotExist:
        messages.error(request, "You are not authorized to enter marks.")
        return redirect('TeacherApp:teacher_login')

    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('TeacherApp:myCourses')

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('TeacherApp:myCourses')
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
