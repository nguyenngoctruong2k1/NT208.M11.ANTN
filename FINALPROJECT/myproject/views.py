from django.db.models import query
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin
from django.views.generic import ListView, DetailView

from myproject.models import MonHoc,FileUpload, TaiLieu,CommentMH
from myproject.forms import ThemMonHoc, ThemTaiLieu, RegisterForm,TL,CommentMHForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import random
import hashlib
import time
from django.contrib import messages

from icecream import ic

from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.


def home_view(request):
    return render(
        request,
        'home.html',
    )

def one_document_view(request, MaTL):
    tai_lieu = TaiLieu.objects.get(MaTL=MaTL)
    return render(
        request,
        'onedocument.html',
        {'tai_lieu': tai_lieu},
    )

def dashboard_view(request):
    #ic(request.user.username)
    if request.method == 'POST':
        form = ThemMonHoc(request.POST)
        if form.is_valid():
            form.save()
    # ic(request.GET['p'])
    form = ThemMonHoc()
    # data = MonHoc.objects.all()
    p = Paginator(MonHoc.objects.all(), 3)
    page = request.GET.get('page')
    monhoc = p.get_page(page)
    overview = {
            'new_doc': TaiLieu.objects.filter(KiemDuyet=True).count(),
            'old_doc': TaiLieu.objects.filter(KiemDuyet=False).count(),
            'num_user': User.objects.filter(is_active=True).count()
        }
    return render(
        request,
        'dashboard.html',
        {
            'form': form,
            'monhoc': monhoc,
            'overview':overview
        }
    )

def mon_cu_the(request):
    return render(
        request,
        'mon_cu_the.html',
    )

def Toan_Tin_KHTN(request):
    return render(
        request,
        'Toan_Tin_KHTN.html',
    )

def DongGopTL_view(request):
    if request.method == 'POST':
        ic(request.POST)
        form = ThemTaiLieu(request.POST)
        if form.is_valid():
            instan = form.save(commit=False)
            instan.MaTL = hashlib.sha1(str(time.time()).encode()).hexdigest()[:15]
            instan.KiemDuyet = False
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

    form = ThemTaiLieu()

def TaiLieu_view(request):
    ic(request.user.username)

    p = Paginator(TaiLieu.objects.filter(KiemDuyet=True),15)
    page = request.GET.get('page')
    tailieu = p.get_page(page)

class SlideListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='Slide')
    template_name = 'Slide.html'
    context_object_name = 'Slide'
    paginate_by = 8

class DeThiListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='DT')
    template_name = 'DeThi.html'
    context_object_name = 'DeThi'
    #paginate_by = 4

class BaiTapListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='BT')
    template_name = 'BaiTap.html'
    context_object_name = 'BaiTap'
    #paginate_by = 4
""" def error(request,*args, **kwargs):
    return render(
        request,
        'error.html'
    ) """

def comment(request,MaMH):
    monhoc = get_object_or_404(MonHoc, MaMH=MaMH)
    form = CommentMHForm()
    if request.method == 'POST':
        form = CommentMHForm(request.POST,MSSV=None, MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request, 'mon_cu_the.html',{"monhoc":monhoc, "form":form})
