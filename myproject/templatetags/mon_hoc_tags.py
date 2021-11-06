from django import template
from myproject.models import Mon_Dai_Cuong, Toan_Tin_KHTN,TaiLieu
register = template.Library()


@register.simple_tag()
def get_mon_hoc():
    return Mon_Dai_Cuong.objects.all()


@register.simple_tag()
def get_toan_tin_khtn():
    return Toan_Tin_KHTN.objects.all()

@register.simple_tag()
def get_tai_lieu():
    return TaiLieu.objects.all().order_by("-date")

@register.simple_tag()
def get_tai_lieu_De_Thi():
    return TaiLieu.objects.filter(LoaiTL='DT').order_by("-date")[:3]

@register.simple_tag()
def get_tai_lieu_Slide():
    return TaiLieu.objects.filter(LoaiTL='Slide').order_by("-date")[:3]

@register.simple_tag()
def get_tai_lieu_Bai_Tap():
    return TaiLieu.objects.filter(LoaiTL='BT').order_by("-date")[:3]
