from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator
)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(

    upload_to='students/',

    validators=[
        FileExtensionValidator(
            allowed_extensions=[
                'jpg',
                'jpeg',
                'png'
            ]
        )
    ],

    blank=True,
    null=True
)
    phone = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    qualification = models.CharField(max_length=200)
    hire_date = models.DateField()
    created_at = models.DateTimeField( auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='students/',blank=True,null=True)
    address = models.TextField()
    admission_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.date}")


class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5,decimal_places=2)
    grade = models.CharField(max_length=5)
    remarks = models.TextField(blank=True)
    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.subject}"
            )
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title