from django.db.models import query
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin
from icecream import ic
from .models import TaiLieu, CommentMH,MonHoc
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .forms import CommentMHForm
from django.http import HttpResponseRedirect
# Create your views here.


def home_view(request):
    return render(
        request,
        'home.html',
    )

def one_document_view(request, MaTL):
    tai_lieu = TaiLieu.objects.get(MaTL=MaTL)
    return render(
        request,
        'onedocument.html',
        {'tai_lieu': tai_lieu},
    )
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

""" def Slide(request):
    return render(
        request,
        'Slide.html',
)  """

class SlideListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='Slide')
    template_name = 'Slide.html'
    context_object_name = 'Slide'
    paginate_by = 8

""" def DeThi(request):
    return render(
        request,
        'DeThi.html',
) """ 

class DeThiListview(ListView):
    queryset = TaiLieu.objects.filter(LoaiTL='DT')
    template_name = 'DeThi.html'
    context_object_name = 'DeThi'
    #paginate_by = 4

""" def BaiTap(request):
    return render(
        request,
        'BaiTap.html',
)  """

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
