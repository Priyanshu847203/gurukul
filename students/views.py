from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Student, Attendance, TestMarks


# ---------------- HOME ----------------
def home(request):
    return render(request, "home.html")


# ---------------- STUDENT REGISTER ----------------
def student_register(request):
    if request.method == "POST":

        if Student.objects.filter(email=request.POST.get("email")).exists():
            return render(request, "student_register.html", {"error": "Email already registered"})

        if Student.objects.filter(roll_no=request.POST.get("roll_no")).exists():
            return render(request, "student_register.html", {"error": "Roll Number already exists"})

        Student.objects.create(
            name=request.POST.get("name"),
            father_name=request.POST.get("father_name"),
            roll_no=request.POST.get("roll_no"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),
            course=request.POST.get("course"),
            password=request.POST.get("password")
        )

        return redirect("student_login")

    return render(request, "student_register.html")


# ---------------- STUDENT LOGIN ----------------
def student_login(request):
    if request.method == "POST":

        student = Student.objects.filter(
            email=request.POST.get("email"),
            password=request.POST.get("password")
        ).first()

        if student:
            request.session["student_id"] = student.id
            return redirect("student_dashboard")

        return render(request, "student_login.html", {"error": "Invalid Email or Password"})

    return render(request, "student_login.html")


# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard(request):
    if "student_id" not in request.session:
        return redirect("student_login")

    return render(request, "student_dashboard.html")


# ---------------- STUDENT ATTENDANCE ----------------
def student_attendance(request):
    if "student_id" not in request.session:
        return redirect("student_login")

    student = get_object_or_404(Student, id=request.session["student_id"])
    today = date.today()

    already = Attendance.objects.filter(student=student, date=today).exists()

    if request.method == "POST":
        if not already:
            Attendance.objects.create(
                student=student,
                status=request.POST.get("status"),
                date=today
            )
        return redirect("student_attendance")

    return render(request, "student_attendance.html", {"already_marked": already})


# ---------------- STUDENT HISTORY ----------------
def student_history(request):
    student = get_object_or_404(Student, id=request.session.get("student_id"))
    attendance = Attendance.objects.filter(student=student).order_by("-date")

    return render(request, "student_history.html", {"attendance": attendance})


# ---------------- STUDENT PROFILE ----------------
def student_profile(request):
    student = get_object_or_404(Student, id=request.session.get("student_id"))

    total = Attendance.objects.filter(student=student).count()
    present = Attendance.objects.filter(student=student, status="Present").count()

    percentage = (present / total * 100) if total > 0 else 0

    return render(request, "student_profile.html", {
        "student": student,
        "percentage": percentage
    })


# ---------------- TEST MARKS ----------------
def student_test_marks(request):
    student = get_object_or_404(Student, id=request.session.get("student_id"))
    marks = TestMarks.objects.filter(student=student)

    return render(request, "student_test_marks.html", {"marks": marks})


# ---------------- STUDENT PERFORMANCE ----------------
def student_performance(request):
    student = get_object_or_404(Student, id=request.session.get("student_id"))
    marks = TestMarks.objects.filter(student=student)

    total_subject = marks.count()
    total_marks = sum(m.marks for m in marks)

    percentage = (total_marks / (total_subject * 100) * 100) if total_subject > 0 else 0

    return render(request, "student_performance.html", {
        "total_subject": total_subject,
        "total_marks": total_marks,
        "percentage": percentage
    })


# ---------------- MONTHLY ATTENDANCE ----------------
# def student_monthly_attendance(request):
#     return render(request, "student_monthly_attendance.html")

from django.shortcuts import get_object_or_404
from .models import Student, Attendance, TestMarks

def student_monthly_attendance(request):

    if "student_id" not in request.session:
        return redirect("student_login")

    student = get_object_or_404(
        Student,
        id=request.session["student_id"]
    )

    attendance = Attendance.objects.filter(
        student=student
    ).order_by("-date")

    total_classes = attendance.count()

    present = attendance.filter(
        status="Present"
    ).count()

    absent = attendance.filter(
        status="Absent"
    ).count()

    percentage = 0

    if total_classes > 0:
        percentage = (present / total_classes) * 100

    marks = TestMarks.objects.filter(
        student=student
    )

    return render(
        request,
        "student_monthly_attendance.html",
        {
            "attendance": attendance,
            "marks": marks,
            "total_classes": total_classes,
            "present": present,
            "absent": absent,
            "percentage": percentage,
        }
    )



# ---------------- TEACHER LOGIN ----------------
def teacher_login(request):
    if request.method == "POST":

        if request.POST.get("teacher_id") == "gurukul@admin" and request.POST.get("password") == "world8809":
            request.session["teacher"] = True
            return redirect("teacher_dashboard")

        return render(request, "teacher_login.html", {"error": "Invalid login"})

    return render(request, "teacher_login.html")


# ---------------- TEACHER DASHBOARD ----------------
def teacher_dashboard(request):
    if "teacher" not in request.session:
        return redirect("teacher_login")

    today = date.today()

    return render(request, "teacher_dashboard.html", {
        "total_students": Student.objects.count(),
        "present_students": Attendance.objects.filter(date=today, status="Present").count(),
        "absent_students": Attendance.objects.filter(date=today, status="Absent").count(),
        "total_tests": TestMarks.objects.count()
    })


# ---------------- TEACHER REGISTER ----------------
from datetime import date
from django.shortcuts import render, redirect
from .models import Student, Attendance

def teacher_mark(request):

    students = Student.objects.all()

    if request.method == "POST":

        today = date.today()

        for student in students:

            status = request.POST.get(
                f"attendance_{student.id}",
                "Absent"
            )

            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={
                    "status": status
                }
            )

        return redirect("teacher_dashboard")

    return render(
        request,
        "teacher_mark.html",
        {
            "students": students
        }
    )

# ---------------- ADD STUDENT ----------------
def add_student(request):
    if "teacher" not in request.session:
        return redirect("teacher_login")

    if request.method == "POST":
        Student.objects.create(
            name=request.POST.get("name"),
            father_name=request.POST.get("father_name"),
            roll_no=request.POST.get("roll_no"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),
            course=request.POST.get("course"),
            password=request.POST.get("password")
        )
        return redirect("manage_students")

    return render(request, "add_student.html")


# ---------------- MANAGE STUDENTS ----------------
def manage_students(request):
    students = Student.objects.all()
    return render(request, "manage_students.html", {"students": students})


# ---------------- ADD MARKS ----------------
def add_marks(request):
    if "teacher" not in request.session:
        return redirect("teacher_login")

    students = Student.objects.all()

    if request.method == "POST":
        student = Student.objects.get(id=request.POST.get("student"))

        TestMarks.objects.create(
            student=student,
            subject=request.POST.get("subject"),
            marks=request.POST.get("marks")
        )

        return redirect("add_marks")

    return render(request, "add_marks.html", {"students": students})


# ---------------- TEACHER ATTENDANCE ----------------
def teacher_attendance(request):
    attendance = Attendance.objects.all().order_by("-date")
    return render(request, "teacher_attendance.html", {"attendance": attendance})


# ---------------- DELETE STUDENT ----------------
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("manage_students")


# ---------------- ABOUT ----------------
def about(request):
    return render(request, "about.html")


# ---------------- CONTACT ----------------
def contact(request):
    return render(request, "contact.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect("home")


def teacher_performance(request):
    if "teacher" not in request.session:
        return redirect("teacher_login")

    students = Student.objects.all()
    data = []

    for student in students:
        marks = TestMarks.objects.filter(student=student)

        total_subject = marks.count()
        total_marks = sum(m.marks for m in marks)

        percentage = (total_marks / (total_subject * 100) * 100) if total_subject > 0 else 0

        result = "Pass"
        if percentage < 33:
            result = "Fail"

        data.append({
            "name": student.name,
            "roll_no": student.roll_no,
            "total_marks": total_marks,
            "percentage": percentage,
            "result": result
        })

    return render(request, "teacher_performance.html", {"data": data})

def teacher_register(request):
    return render(request, "teacher_register.html")