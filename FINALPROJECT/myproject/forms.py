from django import forms
from django.db import models
from django.forms import fields
from myproject.models import MonHoc, TaiLieu, FileUpload

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re


# Create your forms here.

class RegisterForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Mật khẩu')
    password2 = forms.CharField(
        label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        cleaned_data = super(RegisterForm, self).clean()
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],
                                 email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password1'])


class ThemMonHoc(forms.ModelForm):
    class Meta:
        model = MonHoc
        fields = (
            'MaMH', 'TenMH', 'Khoa', 'NhomMH', 'MoTa'
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
        fields = ('TenTL', 'LoaiTL', 'MaMH', 'TacGia', 'MoTa')
        widgets = {
            'TenTL': forms.TextInput(attrs={'class': 'form-control'}),
            'TacGia': forms.TextInput(attrs={'class': 'form-control'}),
            'MaMH': forms.Select(attrs={'class': 'form-control'}),
            'LoaiTL': forms.Select(attrs={'class': 'form-control'}),
            'MoTa': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TL(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('MaTL', 'filename', 'Path', 'FileUL')
        # widgets = {
        #     'TenTL': forms.TextInput(attrs={'class': 'form-control'}),
        #     'TacGia': forms.TextInput(attrs={'class': 'form-control'}),
        #     'MaMH': forms.Select(attrs={'class': 'form-control'}),
        #     'LoaiTL': forms.Select(attrs={'class': 'form-control'}),
        #     'MoTa': forms.Textarea(attrs={'class': 'form-control'}),
        # }


#     def clean_student_code(self):
#         data = self.cleaned_data["student_code"]
#         try:
#             student_code = int(data)
#         except ValueError:
#             raise forms.ValidationError("Mã số sinh viên là một số nguyên")
#         return data
