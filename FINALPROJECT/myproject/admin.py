from django.contrib import admin
from myproject.models import MonHoc, TaiLieu, CommentMH, CommentTL,FileUpload
# from myproject.models import MonHoc, Student, TaiLieu, User, CommentMH, CommentTL

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('HoTen','MSSV','GioiTinh','Email','NgayDK','Khoa','MoTa')
#     search_fields = ('HoTen', 'MSSV','Email','Khoa')
#     list_filter = ('HoTen', 'Khoa')

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('MSSV','Password')

@admin.register(MonHoc)
class MonHocAdmin(admin.ModelAdmin):
    list_display = ('MaMH','TenMH','Khoa','NhomMH','MoTa')

@admin.register(TaiLieu)
class TaiLieuAdmin(admin.ModelAdmin):
    list_display = ('MaTL','TenTL','MaMH','LoaiTL','MoTa','LuotTai','LuotXem')

@admin.register(CommentTL)
class CommentTLAdmin(admin.ModelAdmin):
    list_display = ('MSSV','MaTL','ThoiGian','NoiDung')

@admin.register(CommentMH)
class CommentMHAdmin(admin.ModelAdmin):
    list_display = ('MSSV','MaMH','ThoiGian','NoiDung')

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('MaTL','filename','Path')