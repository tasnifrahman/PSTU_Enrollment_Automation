from django.urls import path
from . import views
app_name = "TeacherApp"
urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('enter_marks/<str:course_code>/', views.enter_marks, name='enter_marks'), 
]
