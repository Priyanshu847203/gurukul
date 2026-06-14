
from django.db import models


# ---------------- STUDENT ----------------

class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    course = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---------------- ATTENDANCE ----------------

class Attendance(models.Model):

    STATUS = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='Absent'
    )

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date}"


# ---------------- TEACHER ----------------

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---------------- TEST MARKS ----------------

class TestMarks(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=50)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"


# ---------------- MONTHLY REPORT ----------------

class MonthlyAttendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    month = models.CharField(max_length=30)

    total_classes = models.IntegerField(default=0)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    attendance_percentage = models.FloatField(default=0)

    def __str__(self):
        return self.student.name



