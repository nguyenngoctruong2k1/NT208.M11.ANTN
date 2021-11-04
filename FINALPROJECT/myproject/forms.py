from django import forms
from django.db import models
from django.forms import fields
from myproject.models import MonHoc, TaiLieu, FileUpload

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff=True
        if commit:
            user.save()
        return user

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
    # myfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = TaiLieu
        fields =('TenTL','LoaiTL','MaMH','TacGia','MoTa')
        widgets = {
            'TenTL': forms.TextInput(attrs={'class': 'form-control'}),
            'TacGia': forms.TextInput(attrs={'class': 'form-control'}),
            'MaMH': forms.Select(attrs={'class': 'form-control'}),
            'LoaiTL': forms.Select(attrs={'class': 'form-control'}),
            'MoTa': forms.Textarea(attrs={'class': 'form-control'}),
            # 'Path': forms.FileField(),
        }

class TL(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields =('MaTL','filename','Path')

    