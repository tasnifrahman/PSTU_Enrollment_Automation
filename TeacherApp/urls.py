from django.urls import path
from . import views
<<<<<<< HEAD
app_name = "TeacherApp"
urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('enter_marks/<str:course_code>/', views.enter_marks, name='enter_marks'), 
    path('logout/', views.teacher_logout, name='teacher_logout'),
]
=======

app_name = "TeacherApp"
urlpatterns = [    
    path('login/', views.teacher_login, name="teacher_login"),
    path('logout/', views.teacher_logout, name="teacher_logout"),
    path('dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    
    path('myCourses/', views.myCourses, name="myCourses"),
    
    path('enterMarks/<str:course_code>/', views.enter_marks, name="enter_marks"),
]
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
