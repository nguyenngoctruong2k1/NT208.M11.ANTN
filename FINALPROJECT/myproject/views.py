from django.db import models
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from icecream import ic
from django.views.generic import ListView 
from django.core.paginator import Paginator
from django.views.generic.edit import ModelFormMixin
from myproject.forms import ThemMonHoc,ThemTaiLieu,NewUserForm,TL
from myproject.models import MonHoc,FileUpload, TaiLieu
import random
import hashlib
import time
from django.contrib.auth import login
from django.contrib import messages

# from myproject.forms import TaoTaiLieu

from django.conf import settings
def simple_upload(request):
    # ic(request.POST['text'])
    ic(bool(request.FILES))  
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES.getlist('myfile')
        fs = FileSystemStorage()
        for f in myfile:
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

class MonHocListView(ListView, ModelFormMixin):
    model = MonHoc
    template_name = 'dashboard.html'
    paginate_by = 2

def DangKy_view(request):
    if request.method == 'POST':
        # ic(request.method)
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "Registration successful." )
            # return redirect("main:homepage")
        else:
            ic(form.errors)
            return render(
                request=request, 
                template_name="DangKy.html", 
                context={"register_form":form, 'form_error':form.errors})
    form = NewUserForm()
    return render (request=request, template_name="DangKy.html", context={"register_form":form, 'form_error':form.errors})

def dashboard_view(request):
    ic(request.user.username)
    if request.method == 'POST':
        form = ThemMonHoc(request.POST)
        if form.is_valid():
            form.save()
    
    # ic(request.GET['p'])
    form = ThemMonHoc()
    # data = MonHoc.objects.all()
    p = Paginator(MonHoc.objects.all(),3)
    page = request.GET.get('page')
    monhoc = p.get_page(page)

    return render(
        request,
        'dashboard.html', 
        {
            'form': form , 
            'monhoc':monhoc
        }
    )

def DuyetTL_view(request):
    return render(
        request,
        'db_DuyetTL.html', {'data':FileUpload.objects.all()}
    )

def DongGopTL_view(request):
    if request.method == 'POST':
        ic(request.POST)
        form = ThemTaiLieu(request.POST)
        if form.is_valid():
            instan = form.save(commit=False)
            instan.MaTL = hashlib.sha1(str(time.time()).encode()).hexdigest()[:15]
            instan.MSSV = request.user.username
            # Lưu file vào cơ sở dữ liệu
            if request.FILES and request.FILES['myfile']:
                myfile = request.FILES.getlist('myfile')
                fs = FileSystemStorage()
                for f in myfile:
                    filename = fs.save(f.name, f)
                    uploaded_file_url = fs.url(filename)
                    file_tai_lieu = TL({'MaTL':instan.MaTL,'filename':filename,'Path':uploaded_file_url})
                    file_tai_lieu.save()
            instan.save()

    else:
        form = ThemTaiLieu()
    return render(
        request, 
        'db_DongGopTL.html', {'form': form}
    )

def TaiLieu_view(request):
    ic(request.user.username)

    p = Paginator(TaiLieu.objects.all(),15)
    page = request.GET.get('page')
    tailieu = p.get_page(page)

    return render(
        request,
        'db_TaiLieu.html',
        {
            'tailieu':tailieu
        }
    )

def TaiLieu_delete(request, slug):  
    tailieu = TaiLieu.objects.get(MaTL=slug)  
    if tailieu: tailieu.delete() 
    fileUp = FileUpload.objects.get(MaTL=slug)
    if fileUp: fileUp.delete()
    return redirect('TaiLieu_view')  

def ThanhVien_view(request):
    return render(
        request,
        'db_ThanhVien.html',
    )
def BinhLuan_view(request):
    return render(
        request,
        'db_BinhLuan.html',
    )

# def DangTaiLieu(request):
#     if request.method == 'POST':
#         form = TaoTaiLieu(request.POST)
#         form.save()
#         if form.is_valid():
#             instance = form.save()
#             instance.birth_place ='HCM'
#             instance.save()
#             # ok_url = reversed('new_student_form_ok')
#             # return redirect('new_student_form_ok.html')
#     else:
#         form = TaoTaiLieu

#     return render(
#         request,
#         'new_student_form.html',
#         {
#             'form':form,
#         }
#     )