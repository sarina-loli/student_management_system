from django.contrib import admin

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

# Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('created_at',)

# Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)

# Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'qualification'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email'
    )

    list_filter = (
        'qualification',
    )

# Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'course'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email'
    )

    list_filter = (
        'gender',
        'course'
    )

# Subject
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'course',
        'teacher'
    )

# Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'date',
        'status'
    )

# Result
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'marks',
        'grade'
    )

# Notice
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at'
    )