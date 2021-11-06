from django.contrib import admin
from myproject.models import MonHoc, Student, TaiLieu, User, CommentMH, CommentTL,Mon_Dai_Cuong,Mon_Chuyen_Nganh,Co_So_Nganh,Co_So_Nhom_Nganh,Toan_Tin_KHTN

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('HoTen','MSSV','GioiTinh','Email','NgayDK','Khoa','MoTa')
    search_fields = ('HoTen', 'MSSV','Email','Khoa')
    list_filter = ('HoTen', 'Khoa')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('MSSV','Password')

@admin.register(MonHoc)
class MonHocAdmin(admin.ModelAdmin):
    list_display = ('MaMH','TenMH','Khoa','NhomMH','MoTa')

@admin.register(TaiLieu)
class TaiLieuAdmin(admin.ModelAdmin):
    list_display = ('MaTL','TenTL','MaMH','LoaiTL','MoTa','LuotTai','LuotXem','Path','date')
    search_fields = ['MaTL']

@admin.register(CommentTL)
class CommentTLAdmin(admin.ModelAdmin):
    list_display = ('MSSV','MaTL','ThoiGian','NoiDung')

@admin.register(CommentMH)
class CommentMHAdmin(admin.ModelAdmin):
    list_display = ('MSSV','MaMH','ThoiGian','NoiDung')

@admin.register(Mon_Chuyen_Nganh)
class Mon_Chuyen_Nganh_Admin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Mon_Dai_Cuong)
class Mon_Dai_Cuong_Admin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Co_So_Nganh)
class Co_So_Nganh_Admin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Co_So_Nhom_Nganh)
class Co_So_Nhom_Nganh_Admin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Toan_Tin_KHTN)
class Toan_Tin_KHTN_Admin(admin.ModelAdmin):
    list_display = ('name',)
