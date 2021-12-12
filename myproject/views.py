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

# Tạo trang chủ
def home_view(request):
    return render(
        request,
        'global_home.html',
    )

# Tạo trang seach
def search_view(request):
    keyword= ''
    if request.method == 'GET':
        # Tiền xử lý từ khóa tìm kiếm
        if request.GET.get("search") != None:
            searched = request.GET.get('search')
        keyword = searched
        searched = unidecode(searched)
        # Nhận kết quả tìm kiếm
        if searched: data = TaiLieu.objects.filter(KiemDuyet=True).filter(Q(search__icontains=searched))
        else: data = TaiLieu.objects.filter(KiemDuyet=True)
        # Phân trang cho kết quả tìm kiếm
        num = 10
        if request.GET.get('num'): num = int(request.GET.get('num'))
        p = Paginator(data, num)
        page = request.GET.get('page')
        tailieu = p.get_page(page)
        # Dữ liệu trả về
        result = {
            'tailieu': tailieu,
            'num': num,
            'length': len(data),
            'keyword':keyword
        }
        # render kết quả trang tìm kiếm trả kết quả tìm kiếm cho người dùng
        return render(
            request,
            'search.html',
            result,
        )
    return render(
        request,
        'search.html',
    )

# Tạo trang hiển thị danh sách các môn học
def MonHocList_view(request, NhomMH, Khoa):
    # Nhận kết quả 
    data = MonHoc.objects.filter(NhomMH=NhomMH).filter(Khoa=Khoa)
    # Thực hiện phân trang 
    num = 10
    if request.GET.get('num'): num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    monhoc = p.get_page(page)
    # Lấy thông tin của request
    khoa = ''
    nhom_mh = ''
    if monhoc:
        khoa = monhoc[0].get_Khoa_display()
        nhom_mh = monhoc[0].get_NhomMH_display()
    # Thực hiện render trả kết quả cho request
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

# Trang mô tả tổng quát về môn học và show một ít tài liệu
def MonHoc_show(request, MaMH):
    # Lấy comment của bài môn học, và xếp theo thời gian
    comment = CommentMH.objects.filter(MaMH=MaMH).order_by("-ThoiGian")
    # Lấy một ít tài liệu để show
    data = TaiLieu.objects.filter(MaMH=MaMH).filter(KiemDuyet=True)
    tailieu = {
        data.filter(LoaiTL='Slide').order_by("-date")[:4],
        data.filter(LoaiTL='DeThi').order_by("-date")[:4],
        data.filter(LoaiTL='BaiTap').order_by("-date")[:4],
        data.filter(LoaiTL='TaiLieuTK').order_by("-date")[:4]
    }
    # Nhận thông tin về môn học
    monhoc = get_object_or_404(MonHoc, MaMH=MaMH)
    # Tạo form bình luận cho user
    form = CommentMHForm()
    # Nhận bình luận của user
    if request.method == 'POST':
        form = CommentMHForm(request.POST, user=request.user, MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    # Lấy thông tin của môn học
    monhoc.len = data.count
    monhoc.download = sum(list(map(lambda item: item[0], data.values_list('LuotTai'))))
    # Render kết quả
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

# Trang trình bày tất cả các tài liệu trong một loại tài liệu của môn học nào đó
def MonHoc_LoaiTL_show(request, MaMH, LoaiTL):
    # Nhận tất cả các comment của môn học
    comment = CommentMH.objects.filter(MaMH=MaMH).order_by("-ThoiGian")
    # Lấy tất cả các tài liệu theo loại tài liệu và mã môn học
    tailieu = TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL)
    # Lấy thông tin của môn học
    monhoc = get_object_or_404(MonHoc,MaMH=MaMH)
    # Xử lý commnent
    if request.method == 'POST':
        form = CommentMHForm(request.POST, user=request.user,MaMH=monhoc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    if not tailieu:
        return HttpResponseRedirect(reverse('error'))
    # Tạo form để nhập bình luận
    form = CommentMHForm()
    # Render kết quả trả về cho request
    return render(
        request,
        'show_MonHoc_LoaiTL.html',
        {
            'monhoc': MonHoc.objects.get(MaMH=MaMH),
            'tailieu': TaiLieu.objects.filter(MaMH=MaMH).filter(LoaiTL=LoaiTL),
            'comment':comment,
            'form':form,
        },
    )

# Trang trình bày một tài liệu cụ thể
def one_document_view(request, slug):
    # Lấy comment và sắp xếp theo thời gian
    comment = CommentTL.objects.filter(MaTL=slug).order_by("-ThoiGian")
    # Lấy thông tin về tài liệu
    tai_lieu = TaiLieu.objects.get(MaTL=slug)
    # Tính năng bài viết đã xem cho user đã login
    if request.user.username:
        RecentView.objects.get_or_create(user = request.user, MaTL_id=slug)
        temp =  RecentView.objects.get(user = request.user, MaTL_id=slug)
        if temp:
            temp.ThoiGian = timezone.now()
            temp.save()
    # Cập nhập lượt xem cho tài liệu
    tai_lieu.LuotXem = tai_lieu.LuotXem + 1
    tai_lieu.save()
    # Load các file tài liệu đính kèm có trong tài liệu
    FileDinhKem = FileUpload.objects.filter(MaTL=slug)
    # Nhận bình luận từ các user
    if request.method == 'POST':
        form = CommentTLForm(request.POST, user=request.user, MaTL=tai_lieu)
        # Lưu form bình luận
        if form.is_valid():
            # Cập nhập thông báo cho người đăng
            thongbao = ThongBao.objects.create(user = tai_lieu.user)
            temp = thongbao
            temp.NoiDung = str(request.user) + " đã bình luận về tài liệu " + tai_lieu.TenTL + " của bạn"
            if request.user.first_name:
                temp.NoiDung = str(request.user.first_name) + " đã bình luận về tài liệu " + tai_lieu.TenTL + " của bạn" 
            temp.save()
            form.save()
    # Load form bình luận cho các user
    form = CommentTLForm()
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

# Trang thông báo lỗi 
def error(request, *args, **kwargs):
    return render(
        request,
        '404.html'
    )

# Trang đăng kí
def DangKy_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Đăng kí thành công. Đăng nhập để tiếp tục')
            return HttpResponseRedirect(reverse('DangNhap_view'))
    else:
        form = RegisterForm()
    return render(
        request,
        'global_DangKy.html',
        # 'global_DangKy copy.html',
        {'form': form}
    )

# Trang tổng quan, thêm môn học - Dashboard
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
    # Kết quả trả về với người dùng cộng tác viên
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
    # Phân trang
    form = ThemMonHoc()
    num = 10
    if request.GET.get('num'):
        num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    monhoc = p.get_page(page)
    # render
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

# API xử lý duyệt tài liệu
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

# Trang xem trước tài liệu trước khi duyệt
def TaiLieu_Preview(request, MaTL):
    # Kiểm tra quyền truy cập
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

# Trang đóng góp tài liệu
def DongGopTL_view(request):
    # Kiểm tra có phải cộng tác viên không 
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    # Xử lý form 
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

# Trang hiển thị danh sách các tài liệu
def TaiLieu_view(request):
    # Kiểm tra quyền 
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    # Lấy thông tin tài liều cần trả về
    data = TaiLieu.objects.filter(KiemDuyet=True).order_by("-date")
    if not request.user.is_staff:
        data = TaiLieu.objects.filter(user=request.user).order_by("-date")
    # Phân trang 
    num = 10
    if request.GET.get('num'):
        num = int(request.GET.get('num'))
    p = Paginator(data, num)
    page = request.GET.get('page')
    tailieu = p.get_page(page)
    # Render kết quả
    return render(
        request,
        'db_TaiLieu.html',
        {
            'tailieu': tailieu,
            'num': num
        }
    )

# API để downdload tài liệu thông qua URL
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

# API xóa tài liệu
def TaiLieu_delete(request, slug):
    '''
    Xử lý cho việc xóa tài liệu
    url: dashboard/TaiLieu/delete/<Mã tài liệu>
    '''
    #  Kiểm tra quyền
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    # Lấy thông tin tài liệu
    tailieu = TaiLieu.objects.get(MaTL=slug)
    # Kiểm tra số lượng tài liệu 
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
        try:
            basePath = os.path.join('document', slug)
            paths = os.path.join(settings.MEDIA_ROOT, basePath)
            shutil.rmtree(paths)
            os.remove(paths+'.zip')
        except:pass
    return redirect('TaiLieu_view')

# API kiểm tra việc đọc thông báo
def Doc_Thong_Bao(request,slug):
    doctb = ThongBao.objects.get(pk=slug)
    doctb.Xem = True
    doctb.save()
    request.reload()
    #return HttpResponseRedirect(request.path)
    return render(request,)

# API thay đổi khóa hoạt động của user
def ThanhVien_Active(request, username):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    user = User.objects.get(username=username)
    user.is_active = not user.is_active
    user.save()
    return HttpResponseRedirect(reverse('ThanhVien_view'))

# API đổi quyền User
def ThanhVien_Staff(request, username):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    user = User.objects.get(username=username)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse('ThanhVien_view'))

# Trang trả kết quả danh sách các thành viên dashboard
def ThanhVien_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard_view'))
    # Phân trang
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

# Thông tin cá nhân
def ThongTinCaNhan_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('DangNhap_view'))
    form = Information()
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
            messages.add_message(request, messages.INFO, 'Cập nhật thông tin thành công')

    return render(
        request,
        'db_ThongTinCaNhan.html',
        {
            "form": form,
            "data": InformationUser.objects.get_or_create(User=request.user),
        }
    )
