from django.db import models
from django.db.models.fields import TimeField
from ckeditor.fields import RichTextField

# class Student(models.Model):
#     """
#     Lưu dữ liệu về sinh viên
#     """
#     HoTen = models.CharField(max_length=30, help_text="Họ và tên của sinh viên.")
#     MSSV = models.CharField(max_length=30,primary_key=True, help_text="Mã số sinh viên.")
#     gender_choices = (
#         ('N','Nam'),
#         ('F','Nữ')
#     )
#     GioiTinh = models.CharField(max_length=1, choices=gender_choices, default='N')
#     Email = models.EmailField(max_length=200,help_text="Địa chỉ email")    
#     NgayDK = models.DateField(blank=True, null=True)
#     Khoa_Choices = (
#         ('CNPM','Công nghệ phần mềm'),
#         ('KTMT','Kỹ thuật máy tính'),
#         ('KHMT','Khoa học máy tính'),
#         ('HTTT','Hệ thống thông tin'),
#         ('MMT&TT','Mạng máy tính và truyền thông'),
#         ('KTTT','Khoa học và kỹ thuật thông tin')
#     )
#     Khoa = models.CharField(max_length=10, choices=Khoa_Choices, default='CNPM')
#     MoTa = models.CharField(max_length=100)
#     def __str__(self):
#         return self.HoTen

# class User(models.Model):
#     """
#     Lưu dữ liệu về người dùng
#     """
#     MSSV = models.CharField(max_length=30,primary_key=True, help_text="Họ và tên của sinh viên.")
#     Password = models.CharField(max_length=130, help_text="Mã số sinh viên.")
#     def __str__(self):
#         return self.MSSV

class MonHoc(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    MaMH = models.CharField(max_length=10,primary_key=True, help_text="Mã môn học")
    TenMH = models.CharField(max_length=150, help_text="Mã số sinh viên.")
    Khoa_Choices = (
        ('CNPM','Công nghệ phần mềm'),
        ('KTMT','Kỹ thuật máy tính'),
        ('KHMT','Khoa học máy tính'),
        ('HTTT','Hệ thống thông tin'),
        ('MMT&TT','Mạng máy tính và truyền thông'),
        ('KTTT','Khoa học và kỹ thuật thông tin')
    )
    Khoa = models.CharField(max_length=10, choices=Khoa_Choices, default='CNPM')
    NhomMH_Choices = (
        ('DC','Môn học đại cương'),
        ('CSNN','Cơ sở nhóm ngành'),
        ('CSN','Cơ sở ngành'),
        ('MCN','Môn chuyên ngành'),
        ('K','Khác')
    )
    NhomMH = models.CharField(max_length=10, choices=NhomMH_Choices, default='DC')
    MoTa = models.TextField()

class TaiLieu(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    MaTL = models.CharField(max_length=20,primary_key=True, help_text="Mã tài liệu")
    TenTL = models.CharField(max_length=150, help_text="Tên tài liệu.")
    MaMH = models.ForeignKey(MonHoc, on_delete=models.PROTECT)
    ThoiGian = models.DateTimeField(blank=True,null=True)
    MSSV = models.CharField(max_length=30, help_text="username người đăng")
    TacGia = models.CharField(max_length=30, help_text="Họ và tên của tác giả.")
    LoaiTL_Choices = (
        ('Slide','Slide bài giảng'),
        ('DT','Đề thi'),
        ('BT','Bài tập'),
        ('TLTK','Tài liệu tham khảo')
    )
    LoaiTL = models.CharField(max_length=10, choices=LoaiTL_Choices, default='Slide')
    # MoTa = models.CharField(max_length=1000)
    MoTa = RichTextField(blank=True,null=True)
    LuotTai = models.DecimalField(max_digits=6,decimal_places=1,default=0)
    LuotXem = models.DecimalField(max_digits=6,decimal_places=1,default=0)
    Path = models.FileField()

class FileUpload(models.Model):
    MaTL = models.CharField(max_length=30, help_text="username người đăng")
    filename = models.CharField(max_length=30, help_text="username người đăng")
    Path = models.CharField(max_length=30, help_text="username người đăng")
    FileUL = models.FileField()

class CommentTL(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    # MSSV = models.ForeignKey(Student,on_delete=models.CASCADE)
    MSSV = models.CharField(max_length=30, help_text="username người đăng")
    MaTL = models.ForeignKey(TaiLieu,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(blank=True,null=True)
    NoiDung = models.TextField()

class CommentMH(models.Model):
    """
    Lưu dữ liệu về môn học
    """
    # MSSV = models.ForeignKey(Student,on_delete=models.CASCADE)
    MSSV = models.CharField(max_length=30, help_text="username người đăng")
    MaMH = models.ForeignKey(MonHoc,on_delete=models.CASCADE)
    ThoiGian = models.DateTimeField(blank=True,null=True)
    NoiDung = models.TextField()