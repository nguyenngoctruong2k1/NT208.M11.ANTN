from django.db.models import query
from django.db.models.fields import FilePathField
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin
from django.views.generic import ListView, DetailView
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from myproject.models import MonHoc,FileUpload, TaiLieu,CommentMH
from myproject.forms import ThemMonHoc, ThemTaiLieu, RegisterForm,TL,CommentMHForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import random
import hashlib
import time
from django.contrib import messages
import os

from icecream import ic

from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.


def home_view(request):
    return render(
        request,
        'home.html',
    )

def MonHocList_view(request,NhomMH,Khoa):
    monhoc = MonHoc.objects.filter(NhomMH=NhomMH).filter(Khoa=Khoa)
    khoa = ''
    nhom_mh = ''
    if monhoc:
        khoa = monhoc[0].get_Khoa_display()
        nhom_mh = monhoc[0].get_NhomMH_display()
    return render(
        request,
        'MonHoc_List.html',
        {
            'khoa': khoa,
            'monhoc': monhoc,
            'nhom_mh':nhom_mh
        },
    )
def MonHoc_show(request,MaMH):
    
    # tailieu = TaiLieu.objects.filter(MaMH=MaMH).filter(KiemDuyet=True)
    # ic(tailieu)

    return render(
        request,
        'mon_cu_the.html',
        {'monhoc': MonHoc.objects.get(MaMH=MaMH)},
    )

def one_document_view(request, slug):
    tai_lieu = TaiLieu.objects.get(MaTL=slug)
    tai_lieu.LuotXem = tai_lieu.LuotXem + 1
    tai_lieu.save()
    return render(
        request,
        'onedocument.html',
        {'tai_lieu': tai_lieu},
    )

def downloadfile(req):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'text.txt'
    filepath = base_dir + '\\myproject\\Files\\' + filename
    # filepath = 
    thefile = filepath
    filename = os.path.basename(thefile)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response

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

class SlideListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='Slide')
    template_name = 'Slide.html'
    context_object_name = 'Slide'
    paginate_by = 4

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


def DangKy_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(
        request,
        # 'DangKy.html',
        'DangKyTruong.html',
        {'form': form}
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
    p = Paginator(MonHoc.objects.all(), 15)
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


def DuyetTL_view(request):
    return render(
        request,
        'db_DuyetTL.html', {'data': FileUpload.objects.all()}
    )


def DongGopTL_view(request):
    if request.method == 'POST':
        ic(request.POST)
        form = ThemTaiLieu(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.MaTL = hashlib.sha1(str(time.time()).encode()).hexdigest()[:15]
            instance.KiemDuyet = False
            instance.date = datetime.datetime.now()
            ic(instance.date)
            instance.user = request.user
            # Lưu file vào cơ sở dữ liệu
            if request.FILES and request.FILES['myfile']:
                myfile = request.FILES.getlist('myfile')
                fs = FileSystemStorage()
                for f in myfile:
                    filename = fs.save(f.name, f)
                    uploaded_file_url = fs.url(filename)
                    file_tai_lieu = TL({'MaTL':instance.MaTL,'filename':filename,'Path':uploaded_file_url})
                    file_tai_lieu.save()
            instance.save()

    form = ThemTaiLieu()
    return render(
        request,
        'db_DongGopTL.html', {'form': form}
    )


def TaiLieu_view(request):
    ic(request.user.username)

    p = Paginator(TaiLieu.objects.filter(KiemDuyet=True),15)
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

