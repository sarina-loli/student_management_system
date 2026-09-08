from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Student,
    Teacher,
    Course,
    Subject,
    Attendance,
    Result,
    Notice,
    Profile,
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
    NoticeForm,
)


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register(request):
    """Register a new user, create their Profile, and log them straight in."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # The post_save signal on User already creates the Profile, but
            # get_or_create keeps this view safe even if signals are ever
            # disabled or run in a different order.
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ---------------------------------------------------------------------------
# Dashboard & profile
# ---------------------------------------------------------------------------

@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_attendance': Attendance.objects.count(),
        'total_results': Result.objects.count(),
        'total_notices': Notice.objects.count(),
        'recent_students': Student.objects.order_by('-created_at')[:5],
        'recent_results': Result.objects.select_related('student', 'subject').order_by('-id')[:5],
        'recent_notices': Notice.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('dashboard')


# ---------------------------------------------------------------------------
# Student CRUD
# ---------------------------------------------------------------------------

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('course')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student added successfully.')
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student deleted.')
        return super().form_valid(form)


@login_required
def student_search(request):
    query = request.GET.get('q')
    students = Student.objects.select_related('course').all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
    return render(request, 'students/student_list.html', {'students': students, 'query': query})


# ---------------------------------------------------------------------------
# Teacher CRUD
# ---------------------------------------------------------------------------

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'students/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset


class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'students/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher added successfully.')
        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'students/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher updated successfully.')
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Course CRUD
# ---------------------------------------------------------------------------

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(code__icontains=query)
            )
        return queryset


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Course added successfully.')
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully.')
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Course deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Subject CRUD
# ---------------------------------------------------------------------------

class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'students/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('course', 'teacher')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(code__icontains=query)
            )
        return queryset


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'students/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject added successfully.')
        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'students/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject updated successfully.')
        return super().form_valid(form)


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Attendance CRUD
# ---------------------------------------------------------------------------

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'students/attendance_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student', 'subject')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(student__first_name__icontains=query)
                | Q(student__last_name__icontains=query)
                | Q(subject__name__icontains=query)
            )
        return queryset


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'students/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Attendance recorded successfully.')
        return super().form_valid(form)


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'students/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Attendance updated successfully.')
        return super().form_valid(form)


class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Attendance record deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Result CRUD
# ---------------------------------------------------------------------------

class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'students/result_list.html'
    context_object_name = 'results'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student', 'subject')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(student__first_name__icontains=query)
                | Q(student__last_name__icontains=query)
                | Q(subject__name__icontains=query)
            )
        return queryset


class ResultCreateView(LoginRequiredMixin, CreateView):
    model = Result
    form_class = ResultForm
    template_name = 'students/result_form.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Result added successfully.')
        return super().form_valid(form)


class ResultUpdateView(LoginRequiredMixin, UpdateView):
    model = Result
    form_class = ResultForm
    template_name = 'students/result_form.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Result updated successfully.')
        return super().form_valid(form)


class ResultDeleteView(LoginRequiredMixin, DeleteView):
    model = Result
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Result deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Notice CRUD
# ---------------------------------------------------------------------------

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'students/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 20


class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'students/notice_form.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notice published successfully.')
        return super().form_valid(form)


class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'students/notice_form.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notice updated successfully.')
        return super().form_valid(form)


class NoticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Notice
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notice deleted.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

@staff_member_required
def admin_report(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_attendance': Attendance.objects.count(),
        'total_results': Result.objects.count(),
        'total_notices': Notice.objects.count(),
    }
    return render(request, 'students/admin_report.html', context)


@login_required
def attendance_report(request):
    attendance = Attendance.objects.select_related('student', 'subject').all()
    return render(request, 'students/attendance_report.html', {'attendance': attendance})


@login_required
def result_report(request):
    results = Result.objects.select_related('student', 'subject').all()
    return render(request, 'students/result_report.html', {'results': results})
