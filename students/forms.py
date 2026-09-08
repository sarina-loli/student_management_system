from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from .models import (
    Profile,
    Student,
    Teacher,
    Course,
    Subject,
    Attendance,
    Result,
    Notice
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = (
            'username','email','password1','password2')
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exists')
        return email

class LoginForm(AuthenticationForm):
    pass

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'profile_picture',
            'phone','address')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        date = cleaned_data.get('date')
        if student and subject and date:
            qs = Attendance.objects.filter(student=student, subject=subject, date=date)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    'Attendance for this student, subject and date already exists.'
                )
        return cleaned_data

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'