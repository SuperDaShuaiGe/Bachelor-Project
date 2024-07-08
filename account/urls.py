from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('upload_guide/', views.upload_guide, name='upload_guide'),
    path('upload_homework/', views.upload_homework, name='upload_homework'),
    path('courses/<int:course_id>/save_guide_changes/', views.save_guide_changes, name='save_guide_changes'),
    path('edit', views.teacher_dashboard2, name='teacher_dashboard2'),
    path('homework', views.homework, name='homework')
]
