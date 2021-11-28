from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from django.utils import timezone
from django.urls import reverse
from wsgiref.util import FileWrapper

from myproject.models import CommentTL, MonHoc,FileUpload, TaiLieu,CommentMH,InformationUser,RecentView,ThongBao
from myproject.forms import ThemMonHoc, ThemTaiLieu, RegisterForm,TL,CommentMHForm,Information, CommentTLForm

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import hashlib
import time
from django.contrib import messages
import os
from django.conf import settings
from django.db.models import Q
from zipfile import ZipFile
from icecream import ic
from unidecode import unidecode
import shutil
from django.http import HttpResponseRedirect,HttpResponse
from wsgiref.util import FileWrapper
from django.db.models import Sum

# Create your views here.


def home_view(request):
    return render(
        request,
        'global_home.html',
    )


# def handler404(request, exception):
#     data = {}
#     return render(request, '404.html', data)


def search_view(request):
    if(request.GET.get("search") == None):
        return render(
            request,
            '#',
        )
    keyword= ''
    if request.method == 'GET' and request.GET.get("search") != None:
        searched = request.GET.get('search')
        keyword = searched
        searched = unidecode(searched)

        if searched:
            # monhoc = MonHoc.objects.filter(Q(search__icontains=searched))
            data = TaiLieu.objects.filter(KiemDuyet=True).filter(Q(search__icontains=searched))

            num = 10
            if request.GET.get('num'): num = int(request.GET.get('num'))
            p = Paginator(data, num)
            page = request.GET.get('page')
            tailieu = p.get_page(page)


            result = {
                # 'monhoc': monhoc,
                'tailieu': tailieu,
                'num': num,
                'length': len(data),
                'keyword':keyword
            }
            return render(
                request,
                'search.html',
                result,
            )
    return HttpResponseRedirect(reverse('search'))


def MonHocList_view(request, NhomMH, Khoa):
    data = MonHoc.objects.filter(NhomMH=NhomMH).filter(Khoa=Khoa)
    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    monhoc = p.get_page(page)


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
            'nhom_mh': nhom_mh,
            'num':num
        },
    )


def MonHoc_show(request, MaMH):
    comment = CommentMH.objects.filter(MaMH=MaMH)
    data = TaiLieu.objects.filter(MaMH=MaMH).filter(KiemDuyet=True)
    
    tailieu = {
        data.filter(LoaiTL='Slide').order_by("-date")[:4],
        data.filter(LoaiTL='DeThi').order_by("-date")[:4],
        data.filter(LoaiTL='BaiTap').order_by("-date")[:4],
        data.filter(LoaiTL='TaiLieuTK').order_by("-date")[:4]
    }

    monhoc = get_object_or_404(MonHoc, MaMH=MaMH)
    form = CommentMHForm()
    if request.method == 'POST':
        form = CommentMHForm(request.POST, user=request.user, MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    monhoc = MonHoc.objects.get(MaMH=MaMH)
    monhoc.len = data.count
    monhoc.download = sum(list(map(lambda item: item[0], data.values_list('LuotTai'))))
    return render(
        request,
        'show_mon_cu_the.html',
        {
            'monhoc': monhoc,
            'tailieu': tailieu,
            'comment': comment,
            'form': form,
        },
    )


def MonHoc_LoaiTL_show(request, MaMH, LoaiTL):
    comment = CommentMH.objects.filter(MaMH=MaMH)
    tailieu = TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL)
    comment = CommentMH.objects.filter(MaMH=MaMH)
    monhoc = get_object_or_404(MonHoc,MaMH=MaMH)
    if request.method == 'POST':
        form = CommentMHForm(request.POST, user=request.user,MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    if not tailieu:
        return HttpResponseRedirect(reverse('error'))
    monhoc = get_object_or_404(MonHoc,MaMH=MaMH)
    form = CommentMHForm()
    if request.method == 'POST':
        form = CommentMHForm(request.POST, user=request.user,MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(
        request,
        'show_MonHoc_LoaiTL.html',
        {
            'comment':comment,
            'monhoc': MonHoc.objects.get(MaMH=MaMH),
            'tailieu': TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL),
            'comment':comment,
            'form':form,
        },
    )


def one_document_view(request, slug):
    comment = CommentTL.objects.filter(MaTL=slug)
    tai_lieu = TaiLieu.objects.get(MaTL=slug)
    if request.user.username:
        RecentView.objects.get_or_create(user = request.user, MaTL_id=slug)
        temp =  RecentView.objects.get(user = request.user, MaTL_id=slug)
        if temp:
            temp.ThoiGian = timezone.now()
            temp.save()
    tai_lieu.LuotXem = tai_lieu.LuotXem + 1
    tai_lieu.save()
    FileDinhKem = FileUpload.objects.filter(MaTL=slug)
    tl = get_object_or_404(TaiLieu, MaTL=slug)
    form = CommentTLForm()
    if request.method == 'POST':
        form = CommentTLForm(request.POST, user=request.user, MaTL=tl)
        if form.is_valid():
            thongbao = ThongBao.objects.create(user = tai_lieu.user)
            temp = thongbao
            temp.NoiDung = str(request.user) + " đã bình luận về tài liệu " + tai_lieu.TenTL + " của bạn"
            if request.user.first_name:
                temp.NoiDung = str(request.user.first_name) + " đã bình luận về tài liệu " + tai_lieu.TenTL + " của bạn" 
            
            temp.save()
            form.save()
            return HttpResponseRedirect(request.path)
    return render(
        request,
        'show_onedocument.html',
        {
            'tai_lieu': tai_lieu,
            'FileDinhKem': FileDinhKem,
            'comment': comment,
            'form': form,
        },
    )


def error(request, *args, **kwargs):
    return render(
        request,
        '404.html'
    )


def DangKy_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Đăng kí thành công. Đăng nhập để tiếp tục')
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
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
            'num_user': User.objects.filter(is_active=True).count(),
            'num_download': TaiLieu.objects.aggregate(Sum('LuotTai'))
        }
    # Kết quả trả về với người dùng thường

    if request.user.is_staff:
        # Nếu là quản trị viên
        if request.method == 'POST':
            form = ThemMonHoc(request.POST)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.search = unidecode(
                    instance.TenMH + ' ' + instance.get_Khoa_display()+' ' + instance.MaMH)
                instance.save()
                messages.add_message(request, messages.INFO,
                                     'Thêm môn học thành công')
            if(form.errors):
                messages.add_message(request, messages.INFO,
                                     'Mã môn học đã tồn tại. Thêm môn học thất bại')
    else:
        tailieu = TaiLieu.objects.filter(user=request.user)
        # Nếu là người dùng thông thường cần phải đổi lại thông tin
        for i in range(len(data)):
            data[i].SoLuongTL = tailieu.filter(MaMH=data[i]).count()
        overview = {
            'new_doc': tailieu.filter(KiemDuyet=False).count(),
            'old_doc': tailieu.filter(KiemDuyet=True).count(),
            'num_user': User.objects.filter(is_active=True).count(),
            'num_download': TaiLieu.objects.aggregate(Sum('LuotTai'))
        }

    # phần xử lý chung
    form = ThemMonHoc()
    num = 10
    if request.GET.get('num'):
        num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    monhoc = p.get_page(page)
    return render(
        request,
        'db_home.html',
        {
            'form': form,
            'monhoc': monhoc,
            'overview': overview,
            'num': num
        }
    )


def DuyetTL_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))

    num = 10
    if request.GET.get('num'):
        num = int(request.GET.get('num'))
    p = Paginator(TaiLieu.objects.filter(KiemDuyet=False), num)
    page = request.GET.get('page')
    tailieu = p.get_page(page)
    form = ThemTaiLieu()
    return render(
        request,
        'db_DuyetTL.html',
        {
            'tailieu': tailieu,
            'form': form,
            'num': num
        }
    )


def TaiLieu_Duyet(request, slug):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    tailieu = TaiLieu.objects.get(MaTL=slug) 
    if tailieu: 
        tailieu.KiemDuyet=True
        thongbao = ThongBao.objects.create(user = tailieu.user)
        temp = thongbao
        temp.NoiDung = "Tài liệu " + tailieu.TenTL +" đã được duyệt" 
        temp.save()
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
            instance.MaTL = hashlib.sha1(
                str(time.time()).encode()).hexdigest()[:15]
            instance.KiemDuyet = False
            if request.user.is_staff:
                instance.KiemDuyet = True
            instance.date = datetime.datetime.now()
            instance.user = request.user
            instance.search = unidecode(
                instance.TenTL + ' ' + instance.get_LoaiTL_display()+' '+instance.MaMH.TenMH + ' ' + instance.MaMH.get_Khoa_display() + instance.MaMH.get_NhomMH_display() + ' ' + (str)(instance.MaMH))
            # Lưu file vào cơ sở dữ liệu
            if request.FILES and request.FILES['myfile']:
                myfile = request.FILES.getlist('myfile')
                fs = FileSystemStorage()

                basePath = os.path.join('document', instance.MaTL)
                zipObj = ZipFile(os.path.join(
                    settings.MEDIA_ROOT, basePath+'.zip'), 'w')
                # Duyệt qua từng file
                for f in myfile:
                    # Lưu vào hệ thống
                    filename = fs.save(os.path.join(basePath, f.name), f)
                    uploaded_file_url = fs.url(filename)
                    # Lưu file vào tập zip
                    zipName = os.path.join(
                        settings.MEDIA_ROOT, os.path.join(basePath, f.name))
                    zipObj.write(zipName, os.path.basename(zipName))
                    # Lưu thông tin của file vào csdl
                    file_tai_lieu = TL(
                        {'MaTL': instance.MaTL, 'filename': os.path.basename(filename), 'Path': uploaded_file_url})
                    file_tai_lieu.save()
                zipObj.close()
            instance.save()
            # Cập nhập số lượng tài liệu cho môn học
            mh = MonHoc.objects.get(MaMH=instance.MaMH)
            mh.SoLuongTL += 1
            mh.save()
            messages.add_message(request, messages.INFO,
                                 'Đóng góp tài liệu thành công')
            return HttpResponseRedirect(reverse('DongGopTL_view'))
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
        data = TaiLieu.objects.filter(user=request.user)

    num = 10
    if request.GET.get('num'):
        num = int(request.GET.get('num'))
    p = Paginator(data, num)

    page = request.GET.get('page')
    tailieu = p.get_page(page)
    return render(
        request,
        'db_TaiLieu.html',
        {
            'tailieu': tailieu,
            'num': num
        }
    )
def TaiLieu_download(request, slug):
    obj = TaiLieu.objects.filter(MaTL=slug)
    if obj:
        instance = TaiLieu.objects.get(MaTL=slug)
        instance.LuotTai += 1
        instance.save()

        basePath = os.path.join('document',slug)
        paths = os.path.join(settings.MEDIA_ROOT,basePath)
        response = HttpResponse(FileWrapper(open(paths+'.zip','rb')), content_type='application/zip')
        return response
    return Http404

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
        mh = MonHoc.objects.get(MaMH=tailieu.MaMH)
        mh.SoLuongTL -= 1
        mh.save()
        # Xóa tài liệu khỏi CSDL
        tailieu.delete()
    # Lấy tất cả các file đính kèm
    fileUp = FileUpload.objects.filter(MaTL=slug)
    if fileUp:
        basePath = os.path.join('document', slug)
        paths = os.path.join(settings.MEDIA_ROOT, basePath)
        shutil.rmtree(paths)
        os.remove(paths+'.zip')
    return redirect('TaiLieu_view')

def Doc_Thong_Bao(request,slug):
    doctb = ThongBao.objects.get(pk=slug)
    doctb.Xem = True
    doctb.save()
    request.reload()
    #return HttpResponseRedirect(request.path)
    return render(request,)

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
    if request.GET.get('num'):
        num = int(request.GET.get('num'))

    p = Paginator(InformationUser.objects.all(), num)

    page = request.GET.get('page')
    data = p.get_page(page)
    for i in range(len(data)):
        data[i].ThoiGianTG = (datetime.datetime.now(
            datetime.timezone.utc) - data[i].User.date_joined).days
        data[i].TaiLieu = TaiLieu.objects.filter(user=data[i].User).count()
        data[i].Comment = CommentMH.objects.filter(user=data[i].User).count()
        data[i].Comment += CommentTL.objects.filter(user=data[i].User).count()

    return render(
        request,
        'db_ThanhVien.html',
        {
            'data': data,
            'num': num
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
            user = User.objects.get(id=request.user.id)
            if request.FILES and request.FILES['Avatar']:
                # Cập nhập avatar nếu có
                f = request.FILES.get('Avatar')
                filename = user.username+os.path.splitext(f.name)[1]
                try:
                    os.remove(os.path.join(
                        settings.MEDIA_ROOT, 'avatar/'+filename))
                except:
                    pass
                fs = FileSystemStorage()
                filename = fs.save('avatar/'+filename, f)
                # Lưu lại thông tin của đường dẫn ảnh
                user.last_name = fs.url(filename)
            # Cập nhập người dùng
            user.first_name = request.POST['Fullname']
            user.email = request.POST['Email']
            user.save()
            # Cập nhập thông tin người dùng
            infoUser = InformationUser.objects.get(User=request.user)
            infoUser.Class = request.POST['Class']
            infoUser.Facebook = request.POST['Facebook']
            infoUser.Github = request.POST['Github']
            infoUser.Bio = request.POST['Bio']
            infoUser.save()
            messages.add_message(request, messages.INFO,
                                 'Cập nhật thông tin thành công')
    form = Information()
    return render(
        request,
        'db_ThongTinCaNhan.html',
        {
            "form": form,
            "data": InformationUser.objects.get_or_create(User=request.user),
        }
    )
