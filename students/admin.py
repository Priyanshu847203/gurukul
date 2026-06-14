from django.contrib import admin
from .models import Student, Attendance, TestMarks

from django.contrib import admin
from .models import MonthlyAttendance

admin.site.register(MonthlyAttendance)

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(TestMarks)

