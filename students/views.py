from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordChangeView

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import (
    Student,
    Teacher,
    Course,
    Subject,
    Attendance,
    Result,
    Notice,
    Profile
)

from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    StudentForm,
    TeacherForm,
    CourseForm,
    SubjectForm,
    AttendanceForm,
    ResultForm,
    NoticeForm
)
def home(request):
    return render(request,'home.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Subject.objects.count()
    total_attendance = Attendance.objects.count()
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_attendance': total_attendance,}
    return render(
        request,
        'dashboard.html',context)

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request,'profile.html',{'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = ('change_password.html')
    success_url = (reverse_lazy('dashboard'))

class StudentListView(ListView):
    model = Student
    template_name = ('student_list.html')
    context_object_name = ('students')

class StudentDetailView(DetailView):
    model = Student
    template_name = ('student_detail.html')

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = ('student_form.html')
    success_url = (reverse_lazy('student_list'))

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = ('student_form.html')
    success_url = (reverse_lazy('student_list'))

class StudentDeleteView(DeleteView):
    model = Student
    template_name = ('confirm_delete.html')
    success_url = (reverse_lazy('student_list'))

class TeacherListView(ListView):
    model = Teacher
    template_name = ('teacher_list.html')

class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = ('teacher_form.html')
    success_url = (reverse_lazy('teacher_list'))

class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = ('teacher_form.html')
    success_url = (reverse_lazy('teacher_list'))

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = ('confirm_delete.html')
    success_url = (reverse_lazy('teacher_list'))

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('course_list')

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('course_list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('course_list')

class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('subject_list')

class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_list.html'
    context_object_name = 'attendance_records'

class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance_form.html'
    success_url = reverse_lazy('attendance_list')
    
class AttendanceUpdateView(UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance_form.html'
    success_url = reverse_lazy('attendance_list')

class AttendanceDeleteView(DeleteView):
    model = Attendance
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('attendance_list')

class ResultListView(ListView):
    model = Result
    template_name = 'result_list.html'
    context_object_name = 'results'

class ResultCreateView(CreateView):
    model = Result
    form_class = ResultForm
    template_name = 'result_form.html'
    success_url = reverse_lazy('result_list')

class ResultUpdateView(UpdateView):
    model = Result
    form_class = ResultForm
    template_name = 'result_form.html'
    success_url = reverse_lazy('result_list')

class ResultDeleteView(DeleteView):
    model = Result
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('result_list')

class NoticeListView(ListView):
    model = Notice
    template_name = 'notice_list.html'
    context_object_name = 'notices'
class NoticeCreateView(CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notice_form.html'
    success_url = reverse_lazy('notice_list')
class NoticeUpdateView(UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notice_form.html'
    success_url = reverse_lazy('notice_list')

class NoticeDeleteView(DeleteView):
    model = Notice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('notice_list')

@login_required
def student_search(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query))
    return render(request,'student_list.html',{'students': students})

@staff_member_required
def admin_report(request):
    return render(request,'admin_report.html')

@login_required
def attendance_report(request):
    attendance = (
        Attendance.objects
        .select_related('student','subject'))
    return render(request,'attendance_report.html',{'attendance': attendance})

@login_required
def result_report(request):
    results = (
        Result.objects
        .select_related('student','subject'))
    return render(
        request,
        'result_report.html',{'results': results})