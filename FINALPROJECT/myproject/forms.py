from django import forms
from django.db import models
from django.forms import fields
from myproject.models import MonHoc, TaiLieu

class ThemMonHoc(forms.ModelForm):
    class Meta:
        model = MonHoc
        fields =(
            'MaMH','TenMH','Khoa','NhomMH','MoTa'
        )
        widgets = {
            'MaMH': forms.TextInput(attrs={'class': 'form-control'}),
            'TenMH': forms.TextInput(attrs={'class': 'form-control'}),
            'Khoa': forms.Select(attrs={'class': 'form-control'}),
            'NhomMH': forms.Select(attrs={'class': 'form-control'}),
            'MoTa': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ThemTaiLieu(forms.ModelForm):
    class Meta:
        model = TaiLieu
        fields =('TenTL','LoaiTL','MaMH','TacGia','MoTa')
        widgets = {
            'TenTL': forms.TextInput(attrs={'class': 'form-control'}),
            'TacGia': forms.TextInput(attrs={'class': 'form-control'}),
            'MaMH': forms.Select(attrs={'class': 'form-control'}),
            'LoaiTL': forms.Select(attrs={'class': 'form-control'}),
            'MoTa': forms.Textarea(attrs={'class': 'form-control'}),
        }


#     def clean_student_code(self):
#         data = self.cleaned_data["student_code"]
#         try:
#             student_code = int(data)
#         except ValueError:
#             raise forms.ValidationError("Mã số sinh viên là một số nguyên")
#         return data
    