from django import forms
from django.db import models
from django.forms import fields
from TestApp.models import Student

class CreateNewStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'name', 
            'student_code', 
            'gender', 
            'birth_place',
            'khoa'
        )
    def clean_student_code(self):
        data = self.cleaned_data["student_code"]
        try:
            student_code = int(data)
        except ValueError:
            raise forms.ValidationError("Mã số sinh viên là một số nguyên")
        return data
    