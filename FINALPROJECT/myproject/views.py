import re
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
from myproject.models import CommentTL, InformationUser, MonHoc,FileUpload, TaiLieu,CommentMH,InformationUser
from myproject.forms import ThemMonHoc, ThemTaiLieu, RegisterForm,TL,CommentMHForm,Information
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import random
import hashlib
import time
from django.contrib import messages
import os
from django.conf import settings
from PIL import Image
from django.db.models import Count
from zipfile import ZipFile
from icecream import ic

import shutil

from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.


def home_view(request):
    ic(User._meta.get_fields())
    return render(
        request,
        'global_home.html',
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
        'show_MonHoc_List.html',
        {
            'khoa': khoa,
            'monhoc': monhoc,
            'nhom_mh':nhom_mh
        },
    )
def MonHoc_show(request,MaMH):
    data = TaiLieu.objects.filter(MaMH=MaMH).filter(KiemDuyet=True)
    tailieu ={ 
        data.filter(LoaiTL='Slide').order_by("-date")[:4],
        data.filter(LoaiTL='DeThi').order_by("-date")[:4], 
        data.filter(LoaiTL='BaiTap').order_by("-date")[:4], 
        data.filter(LoaiTL='TaiLieuTK').order_by("-date")[:4]
    }
    ic(tailieu)
    # tailieu = TaiLieu.objects.filter(MaMH=MaMH).filter(KiemDuyet=True)
    # ic(tailieu)

    return render(
        request,
        'show_mon_cu_the.html',
        {
            'monhoc': MonHoc.objects.get(MaMH=MaMH),
            'tailieu': tailieu
        },
    )
def MonHoc_LoaiTL_show(request,MaMH,LoaiTL):
    tailieu = TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL)
    if not tailieu:
        return HttpResponseRedirect(reverse('error'))
    return render(
        request,
        'show_MonHoc_LoaiTL.html',
        {
            'monhoc': MonHoc.objects.get(MaMH=MaMH),
            'tailieu': TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL)
        },
    )

def one_document_view(request, slug):
    tai_lieu = TaiLieu.objects.get(MaTL=slug)
    tai_lieu.LuotXem = tai_lieu.LuotXem + 1
    tai_lieu.save()
    FileDinhKem = FileUpload.objects.filter(MaTL=slug)
    return render(
        request,
        'show_onedocument.html',
        {
            'tai_lieu': tai_lieu,
            'FileDinhKem':FileDinhKem
        },
    )

# def downloadfile(req):
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     filename = 'text.txt'
#     filepath = base_dir + '\\myproject\\Files\\' + filename
#     # filepath = 
#     thefile = filepath
#     filename = os.path.basename(thefile)
#     chunk_size = 8192
#     response = StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
#     response['Content-Length'] = os.path.getsize(thefile)
#     response['Content-Disposition'] = "Attachment;filename=%s" % filename
#     return response

# def mon_cu_the(request):
#     return render(
#         request,
#         'mon_cu_the.html',

#     )

# def Toan_Tin_KHTN(request):
#     return render(
#         request,
#         'Toan_Tin_KHTN.html',
#     )

# class SlideListview(ListView):
#     queryset = TaiLieu.objects.filter(LoaiTL='Slide')
#     template_name = 'Slide.html'
#     context_object_name = 'Slide'
#     paginate_by = 4

# class DeThiListview(ListView):
#     queryset = TaiLieu.objects.filter(LoaiTL='DT')
#     template_name = 'DeThi.html'
#     context_object_name = 'DeThi'
#     #paginate_by = 4

# class BaiTapListview(ListView):
#     queryset = TaiLieu.objects.filter(LoaiTL='BT')
#     template_name = 'BaiTap.html'
#     context_object_name = 'BaiTap'
#     #paginate_by = 4
def error(request,*args, **kwargs):
    return render(
    request,
    'show_error.html'
)

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
        'global_DangKy.html',
        # 'global_DangKy copy.html',
        {'form': form}
    )

def dashboard_view(request):
    # nếu không có tài khoản thì trả về trang đăng nhập
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    # lấy dữ liệu môn học
    data = MonHoc.objects.all()
    overview = {
            'new_doc': TaiLieu.objects.filter(KiemDuyet=False).count(),
            'old_doc': TaiLieu.objects.filter(KiemDuyet=True).count(),
            'num_user': User.objects.filter(is_active=True).count()
        }
    # Kết quả trả về với người dùng thường
    
    if request.user.is_staff:
        # Nếu là quản trị viên
        if request.method == 'POST':
            form = ThemMonHoc(request.POST)
            if form.is_valid():
                form.save()
    else:
        tailieu = TaiLieu.objects.filter(user=request.user)
        # Nếu là người dùng thông thường cần phải đổi lại thông tin
        for i in range(len(data)):
            data[i].SoLuongTL = tailieu.filter(MaMH = data[i]).count()
        overview = {
                'new_doc': tailieu.filter(KiemDuyet=False).count(),
                'old_doc': tailieu.filter(KiemDuyet=True).count(),
                'num_user': User.objects.filter(is_active=True).count()
            }
    
    # phần xử lý chung
    form = ThemMonHoc()
    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    monhoc = p.get_page(page)
    return render(
        request,
        'db_home.html',
        {
            'form': form,
            'monhoc': monhoc,
            'overview':overview,
            'num':num
        }
    )


def DuyetTL_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    
    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))
    p = Paginator(TaiLieu.objects.filter(KiemDuyet=False),num)
    page = request.GET.get('page')
    tailieu = p.get_page(page)
    form = ThemTaiLieu()
    return render(
        request,
        'db_DuyetTL.html', 
        {
            'tailieu': tailieu,
            'form': form,
            'num':num
        }
    )
def TaiLieu_Duyet(request, slug):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    
    tailieu = TaiLieu.objects.get(MaTL=slug)  
    if tailieu: tailieu.KiemDuyet=True
    tailieu.save()
    return redirect('DuyetTL_view') 

def TaiLieu_Preview(request, MaTL):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))

    tailieu = TaiLieu.objects.get(MaTL=MaTL) 
    fileTL = FileUpload.objects.filter(MaTL=MaTL)
    return render(
        request,
        'db_TaiLieu_Preview.html', 
        {
            'form': tailieu,
            'file': fileTL
        }
    ) 

def DongGopTL_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))

    if request.method == 'POST':
        # Lấy thông tin từ form
        form = ThemTaiLieu(request.POST)
        if form.is_valid():
            # Thêm vào các trường thông tin cần thiết cho dữ liệu
            instance = form.save(commit=False)
            instance.MaTL = hashlib.sha1(str(time.time()).encode()).hexdigest()[:15]
            instance.KiemDuyet = False
            instance.date = datetime.datetime.now()
            instance.user = request.user
            # Lưu file vào cơ sở dữ liệu
            if request.FILES and request.FILES['myfile']:
                myfile = request.FILES.getlist('myfile')
                fs = FileSystemStorage()
                
                basePath = os.path.join('document',instance.MaTL)
                zipObj = ZipFile(os.path.join(settings.MEDIA_ROOT,basePath+'.zip'), 'w')
                # Duyệt qua từng file
                for f in myfile:
                    # Lưu vào hệ thống
                    filename = fs.save(os.path.join(basePath,f.name), f)
                    uploaded_file_url = fs.url(filename)
                    # Lưu file vào tập zip
                    zipName = os.path.join(settings.MEDIA_ROOT,os.path.join(basePath,f.name))
                    zipObj.write(zipName,os.path.basename(zipName))
                    # Lưu thông tin của file vào csdl
                    file_tai_lieu = TL({'MaTL':instance.MaTL,'filename':filename,'Path':uploaded_file_url})
                    file_tai_lieu.save()
                zipObj.close()
            instance.save()
            # Cập nhập số lượng tài liệu cho môn học
            mh = MonHoc.objects.get(MaMH = instance.MaMH)
            mh.SoLuongTL +=1
            mh.save()
    form = ThemTaiLieu()
    return render(
        request,
        'db_DongGopTL.html', 
        {'form': form}
    )


def TaiLieu_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))

    data = TaiLieu.objects.filter(KiemDuyet=True)
    if not request.user.is_staff:
        data = data.filter(user = request.user)

    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))
    p = Paginator(data,num)
    page = request.GET.get('page')
    tailieu = p.get_page(page)
    return render(
        request,
        'db_TaiLieu.html',
        {
            'tailieu':tailieu,
            'num':num
        }
    )

def TaiLieu_delete(request, slug):  
    '''
    Xử lý cho việc xóa tài liệu
    url: dashboard/TaiLieu/delete/<Mã tài liệu>
    '''
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))

    tailieu = TaiLieu.objects.get(MaTL=slug)  
    if tailieu:
        # Giảm số lượng tài liệu của môn học 
        mh = MonHoc.objects.get(MaMH = tailieu.MaMH)
        mh.SoLuongTL -=1
        mh.save()
        # Xóa tài liệu khỏi CSDL
        tailieu.delete()
    # Lấy tất cả các file đính kèm
    fileUp = FileUpload.objects.filter(MaTL=slug)
    if fileUp:
        basePath = os.path.join('document',slug)
        paths = os.path.join(settings.MEDIA_ROOT,basePath)
        shutil.rmtree(paths)
        os.remove(paths+'.zip')
    return redirect('TaiLieu_view')  

def ThanhVien_Active(request, username):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    user = User.objects.get(username=username)
    user.is_active = not user.is_active
    user.save()
    return HttpResponseRedirect(reverse('ThanhVien_view'))

def ThanhVien_Staff(request, username):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    user = User.objects.get(username=username)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse('ThanhVien_view'))
        
def ThanhVien_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    
    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))

    p = Paginator(InformationUser.objects.all(),num)
    page = request.GET.get('page')
    data = p.get_page(page)
    for i in range(len(data)):
        data[i].ThoiGianTG= (datetime.datetime.now(datetime.timezone.utc)- data[i].User.date_joined).days
        data[i].TaiLieu = TaiLieu.objects.filter(user=data[i].User).count()
        data[i].Comment = CommentMH.objects.filter(user=data[i].User).count()
        data[i].Comment += CommentTL.objects.filter(user=data[i].User).count()

    # ic(InformationUser.objects.all())
    return render(
        request,
        'db_ThanhVien.html',
        {
            'data':data,
            'num':num
        }
    )


def BinhLuan_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    return render(
        request,
        'db_BinhLuan.html',
    )


def ThongTinCaNhan_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))

    if request.method == 'POST':
        # Lấy thông tin về form
        form = Information(request.POST)
        if form.is_valid:
            # Lấy thông tin người dùng
            user = User.objects.get(id = request.user.id)
            if request.FILES and request.FILES['Avatar']:
                # Cập nhập avatar nếu có
                f = request.FILES.get('Avatar')
                filename = user.username+os.path.splitext(f.name)[1]
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'avatar/'+filename))
                except: pass
                fs = FileSystemStorage()
                filename = fs.save('avatar/'+filename, f)
                # Lưu lại thông tin của đường dẫn ảnh
                user.last_name = fs.url(filename)
            # Cập nhập người dùng
            user.first_name = request.POST['Fullname']
            user.email = request.POST['Email']
            user.save()
            # Cập nhập thông tin người dùng
            infoUser = InformationUser.objects.get(User = request.user)
            infoUser.Class = request.POST['Class']
            infoUser.Facebook = request.POST['Facebook']
            infoUser.Github = request.POST['Github']
            infoUser.Bio = request.POST['Bio']
            infoUser.save()
    form = Information()
    return render(
        request,
        'db_ThongTinCaNhan.html',
        {
            "form":form,
            "data":InformationUser.objects.get_or_create(User=request.user),
        }
    )
