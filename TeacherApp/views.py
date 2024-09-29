from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from TeacherApp.models import Teacher, Course_Instructor
from StudentApp.models import Student
from ResultApp.models import Course_Mark
from django.views.decorators.cache import never_cache

# Teacher Login View
@never_cache  # Prevents caching of the login page
def teacher_login(request):
    # If the user is already logged in, redirect to the dashboard
    if request.user.is_authenticated:
        return redirect('TeacherApp:teacher_dashboard')  # Redirect to teacher dashboard
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a teacher
            if Teacher.objects.filter(user=user).exists():
                login(request, user)
                return redirect('TeacherApp:teacher_dashboard')  # Redirect after login
            else:
                messages.error(request, 'You do not have permission to log in as a teacher.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'teacher_app/teacher_login.html')


# Teacher Logout View
@login_required(login_url='TeacherApp:teacher_login')  # Redirect to login if not authenticated
def teacher_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')  # Optional success message
    
    # Clear Cache on Logout
    response = redirect('TeacherApp:teacher_login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
    response['Pragma'] = 'no-cache'  # HTTP 1.0
    response['Expires'] = '0'  # Proxies
    
    return response


# Teacher Dashboard View
@login_required(login_url='TeacherApp:teacher_login')
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        # Fetch all courses assigned to the teacher
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
        # Get the logged-in teacher
        teacher = Teacher.objects.get(user=request.user)

        # Fetch the selected course instructor entry based on the course code
        course_instructor = get_object_or_404(Course_Instructor, courseinfo__course_code=course_code, teacher_id=teacher)

        # Get all students enrolled in the course
        students = Student.objects.filter(curr_semester=course_instructor.courseinfo.semester)

        if request.method == 'POST':
            # Iterate over each student and save the input marks
            for student in students:
                attendance = request.POST.get(f'attendance_{student.id}')
                assignment = request.POST.get(f'assignment_{student.id}')
                mid_exam = request.POST.get(f'mid_exam_{student.id}')
                final_exam = request.POST.get(f'final_exam_{student.id}')

                # Create or update the marks for each student
                Course_Mark.objects.update_or_create(
                    course_id=course_instructor.courseinfo,  # Reference courseinfo correctly
                    student_id=student,
                    defaults={
                        'attendance': attendance,
                        'assignment': assignment,
                        'mid_exam': mid_exam,
                        'final_exam': final_exam,
                        'total': float(attendance) + float(assignment) + float(mid_exam) + float(final_exam)
                    }
                )

            messages.success(request, 'Marks have been successfully entered.')
            return redirect('TeacherApp:teacher_dashboard')

        # Render the template with the course and student data
        return render(request, 'teacher_app/enter_marks.html', {
            'course_instructor': course_instructor,
            'students': students
        })
    except Teacher.DoesNotExist:
        messages.error(request, 'You do not have access to enter marks for this course.')
        return redirect('TeacherApp:teacher_dashboard')