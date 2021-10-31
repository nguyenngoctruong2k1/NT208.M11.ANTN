from django.urls import path
from TestApp import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-new-student/', views.create_new_student_view, name='create_new_student_view'),
    path('create-new-student/ok/', views.new_student_form_ok, name='new_student_form_ok'),
]
