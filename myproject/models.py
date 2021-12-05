from re import search
from django.db import models
from django.db.models.fields import CharField, TimeField
from django.template.defaultfilters import default, slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.http import request
from unidecode import unidecode


class MonHoc(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    MaMH = models.CharField(max_length=10, primary_key=True, help_text="NT208")
    TenMH = models.CharField(
        max_length=150, help_text="Lập trình ứng dụng web")
    Khoa_Choices = (
        ('CongNghePhanMem', 'Công nghệ phần mềm'),
        ('KyThuatMayTinh', 'Kỹ thuật máy tính'),
        ('KhoaHocMayTinh', 'Khoa học máy tính'),
        ('HeThongThongTin', 'Hệ thống thông tin'),
        ('MangMayTinhTruyenThong', 'Mạng máy tính và truyền thông'),
        ('KyThuatThongTin', 'Khoa học và kỹ thuật thông tin'),
        ('LyLuanChinhTri', 'Lý luận chính trị'),
        ('ToanTinKHTN', 'Toán - Tin học - KHTN'),
        ('NgoaiNgu', 'Ngoại ngữ'),
        ('Khac', 'Khác')
    )
    Khoa = models.CharField(
        max_length=30, choices=Khoa_Choices, default='Khac')

    NhomMH_Choices = (
        ('GiaoDucDaiCuong', 'Giáo dục đại cương'),
        ('CoSoNhomNganh', 'Cơ sở nhóm ngành'),
        ('CoSoNganh', 'Cơ sở ngành'),
        ('ChuyenNganh', 'Chuyên ngành'),
        ('Khac', 'Khác')
    )
    NhomMH = models.CharField(
        max_length=30, choices=NhomMH_Choices, default='Khac')
    MoTa = models.CharField(
        max_length=1000, help_text="Mô tả tổng quan về môn học, khối kiến thức sẽ được học...")
    SoLuongTL = models.IntegerField(default=0)
    search = models.TextField()
    # @property
    # def search(self):
    #     return self.search

    # @search.setter
    # def search(self):
    #     self.search = unidecode(self.TenMH)

    def __str__(self):
        return self.MaMH


class TaiLieu(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    MaTL = models.CharField(max_length=20, primary_key=True)
    TenTL = models.CharField(
        max_length=150, help_text="Slide bài giảng lập trình ứng dụng web.")
    MaMH = models.ForeignKey(MonHoc, on_delete=models.PROTECT)
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    TacGia = models.CharField(max_length=30, help_text="Nguyễn Văn A")
    LoaiTL_Choices = (
        ('Slide', 'Slide'),
        ('DeThi', 'Đề thi'),
        ('BaiTap', 'Bài tập'),
        ('TaiLieuTK', 'Tài liệu tham khảo')
    )
    LoaiTL = models.CharField(
        max_length=10, choices=LoaiTL_Choices, default='Slide')
    MoTa = RichTextField(blank=True, null=True,
                         help_text="Thông tin về tài liệu")
    LuotTai = models.IntegerField(null=True, blank=True, default=0)
    LuotXem = models.IntegerField(null=True, blank=True, default=0)
    KiemDuyet = models.BooleanField(default=False)
    search = models.TextField()


class FileUpload(models.Model):
    MaTL = models.CharField(max_length=30)
    filename = models.CharField(max_length=100)
    Path = models.CharField(max_length=130, primary_key=True)


class CommentTL(models.Model):
    """
    Lưu dữ liệu về những comment dữ liệu 
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    MaTL = models.ForeignKey(TaiLieu,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(auto_now_add=True)
    NoiDung = models.TextField()


class CommentMH(models.Model):
    """
    Lưu dữ liệu về những comment môn học 
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    MaMH = models.ForeignKey(MonHoc,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(auto_now_add=True)
    NoiDung = models.TextField()

class RecentView(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    MaTL = models.ForeignKey(TaiLieu,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(auto_now_add=True)

class ThongBao(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(auto_now_add=True)
    NoiDung = models.TextField()
    Xem = models.BooleanField(default=False)

class InformationUser(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Class = models.CharField(max_length=20)
    Gender_Choices = (
        ('Nam', 'Nam'),
        ('Nu', 'Nữ'),
        ('Khac', 'Khác'),
    )
    Gender = models.CharField(
        max_length=10, choices=Gender_Choices, default='Nam')
    Facebook = models.CharField(max_length=100, default="")
    Github = models.CharField(max_length=100, default="")
    Bio = models.TextField()
