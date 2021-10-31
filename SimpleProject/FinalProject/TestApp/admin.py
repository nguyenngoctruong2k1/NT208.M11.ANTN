from django.contrib import admin
from TestApp.models import Student, Khoa

@admin.register(Khoa)
class KhoaAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','student_code')
    

    

