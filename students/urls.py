from django.urls import path
from . import views

urlpatterns = [

    # ---------------- HOME ----------------
    path('', views.home, name="home"),

    # ---------------- STUDENT ----------------
    path('student/register/', views.student_register, name="student_register"),
    path('student/login/', views.student_login, name="student_login"),
    path('student/dashboard/', views.student_dashboard, name="student_dashboard"),

    path('student/attendance/', views.student_attendance, name="student_attendance"),
    path('student/history/', views.student_history, name="student_history"),
    path('student/profile/', views.student_profile, name="student_profile"),
    path('student/test-marks/', views.student_test_marks, name="student_test_marks"),
    path('student/performance/', views.student_performance, name="student_performance"),
    path('student/monthly-attendance/', views.student_monthly_attendance, name="student_monthly_attendance"),

    # ---------------- PAGES ----------------
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

    # ---------------- TEACHER ----------------
    path('teacher/login/', views.teacher_login, name="teacher_login"),
    path('teacher/dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path(
    'teacher/mark/',
    views.teacher_mark,
    name='teacher_mark'
),
    

    path('teacher/add_student/', views.add_student, name="add_student"),
    path('teacher/manage_students/', views.manage_students, name="manage_students"),
    path('teacher/attendance/', views.teacher_attendance, name="teacher_attendance"),
    path('teacher/add_marks/', views.add_marks, name="add_marks"),
    path('teacher/performance/', views.teacher_performance, name="teacher_performance"),
 


    # ---------------- DELETE ----------------
    path('teacher/delete_student/<int:id>/', views.delete_student, name='delete_student'),

    # ---------------- LOGOUT ----------------
    path('logout/', views.logout_view, name="logout"),
]