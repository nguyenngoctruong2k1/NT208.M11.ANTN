from django import template
from bs4 import BeautifulSoup
# from myproject.models import Mon_Dai_Cuong, Toan_Tin_KHTN,TaiLieu
from myproject.models import MonHoc, TaiLieu,RecentView,ThongBao
register = template.Library()


@register.simple_tag()
def get_mon_hoc():
    return MonHoc.objects.all()

@register.simple_tag()
def get_recent():
    return RecentView.objects.all().order_by("-ThoiGian")[:5]

@register.simple_tag()
def get_thongbao(user):
    return ThongBao.objects.filter(Xem=False).filter(user=user).order_by("-ThoiGian")[:5]
@register.simple_tag()
def get_thongbao_count(user):
    return ThongBao.objects.filter(Xem=False).filter(user=user).count()

@register.simple_tag()
def get_toan_tin_khtn():
    return MonHoc.objects.filter(Khoa='TT')

@register.simple_tag()
def get_tai_lieu():
    return TaiLieu.objects.all().order_by("-date")[:5]

@register.simple_tag()
def get_tai_lieu_De_Thi():
    return TaiLieu.objects.filter(LoaiTL='DT').filter(KiemDuyet=True).order_by("-date")[:3]

@register.simple_tag()
def get_tai_lieu_Slide():
    return TaiLieu.objects.filter(LoaiTL='Slide').filter(KiemDuyet=True).order_by("-date")[:3]

@register.simple_tag()
def get_tai_lieu_Bai_Tap():
    return TaiLieu.objects.filter(LoaiTL='BT').filter(KiemDuyet=True).order_by("-date")[:3]

@register.simple_tag()
def GetMonHocCSNN():
    return MonHoc.objects.filter(NhomMH='CoSoNhomNganh')