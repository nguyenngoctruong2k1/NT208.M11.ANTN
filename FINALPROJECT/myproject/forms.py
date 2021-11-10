
from django.http import request
from myproject.models import CommentMH, InformationUser
from django import forms
from django.db import models
from django.forms import fields
from myproject.models import MonHoc, TaiLieu, FileUpload

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re
from icecream import ic

class CommentMHForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.MSSV = kwargs.pop('MSSV',None)
        self.MaMH = kwargs.pop('MaMH',None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.MSSV = self.MSSV
        comment.MaMH = self.MaMH
        comment.save()
    class Meta:
        model = CommentMH 
        fields = ["NoiDung"]

# Create your forms here.

class RegisterForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Tài khoản", 'required':"required"}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':"Email", 'required':"required"}))
    password1 = forms.CharField(
        label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Mật khẩu", 'required':"required"}))
    password2 = forms.CharField(
        label='Nhập lại mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Nhập lại mật khẩu", 'required':"required"}))

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
        tmp = User.objects.get(username=self.cleaned_data['username'])
        InformationUser.objects.create(User=tmp)


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
            'MoTa': forms.Textarea(attrs={'class': 'form-control'})
        }

class TL(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields =('MaTL','filename','Path')

class Information(forms.Form):
    Avatar = forms.ImageField()
    Fullname = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Tài khoản" }))
    Gender_Choices = (
        ('Nam','Nam'),
        ('Nu','Nữ'),
        ('Khac','Khác'),
    )
    Class = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Tài khoản"}))
    Facebook = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Tài khoản"}))
    Github = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Tài khoản"}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':"Tài khoản"}))
    Bio = forms.CharField(max_length=1000,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':"Tài khoản"}))
