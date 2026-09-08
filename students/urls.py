from django.urls import path

from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('profile/', profile,name='profile'),
    path('change-password/',CustomPasswordChangeView.as_view(),name='change_password'),

]
urlpatterns += [
    path('students/',StudentListView.as_view(),name='student_list'),
    path('students/add/',StudentCreateView.as_view(),name='student_add'),
    path('students/<int:pk>/',StudentDetailView.as_view(),name='student_detail'),
    path('students/<int:pk>/edit/',StudentUpdateView.as_view(),name='student_edit'),
    path('students/<int:pk>/delete/',StudentDeleteView.as_view(), name='student_delete'),
    path('students/search/',student_search,name='student_search'),
]
urlpatterns += [
    path( 'teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/',TeacherCreateView.as_view(),name='teacher_add'),
    path('teachers/<int:pk>/edit/',TeacherUpdateView.as_view(),name='teacher_edit'),
    path('teachers/<int:pk>/delete/',TeacherDeleteView.as_view(),name='teacher_delete'),
]
urlpatterns += [
    path('courses/',CourseListView.as_view(),name='course_list'),
    path('courses/add/',CourseCreateView.as_view(),name='course_add'),
    path('courses/<int:pk>/edit/',CourseUpdateView.as_view(),name='course_edit'),
    path('courses/<int:pk>/delete/',CourseDeleteView.as_view(),name='course_delete'),
]
urlpatterns += [
    path('subjects/',SubjectListView.as_view(),name='subject_list'),
    path('subjects/add/',SubjectCreateView.as_view(),name='subject_add'),
    path('subjects/<int:pk>/edit/',SubjectUpdateView.as_view(),name='subject_edit'),
    path('subjects/<int:pk>/delete/',SubjectDeleteView.as_view(),name='subject_delete'),
]
urlpatterns += [
    path('attendance/',AttendanceListView.as_view(),name='attendance_list'),
    path('attendance/add/',AttendanceCreateView.as_view(),name='attendance_add'),
    path('attendance/<int:pk>/edit/',AttendanceUpdateView.as_view(),name='attendance_edit'),
    path( 'attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='attendance_delete'),
]
urlpatterns += [
    path('results/',ResultListView.as_view(),name='result_list'),
    path('results/add/',ResultCreateView.as_view(),name='result_add'),
    path('results/<int:pk>/edit/',ResultUpdateView.as_view(),name='result_edit'),
    path('results/<int:pk>/delete/',ResultDeleteView.as_view(),name='result_delete'),
]
urlpatterns += [
    path('notices/',NoticeListView.as_view(),name='notice_list'),
    path('notices/add/',NoticeCreateView.as_view(),name='notice_add'),
    path('notices/<int:pk>/edit/',NoticeUpdateView.as_view(),name='notice_edit'),
    path('notices/<int:pk>/delete/',NoticeDeleteView.as_view(),name='notice_delete'),
]
urlpatterns += [
    path('reports/attendance/',attendance_report,name='attendance_report'),
    path('reports/results/',result_report,name='result_report'),
    path('reports/admin/',admin_report,name='admin_report'),
]
