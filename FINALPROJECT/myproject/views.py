from django.db import models
from django.shortcuts import redirect, render
from icecream import ic
from django.views.generic import ListView 
from django.core.paginator import Paginator
from django.views.generic.edit import ModelFormMixin
from myproject.forms import ThemMonHoc,ThemTaiLieu
from myproject.models import MonHoc

# from myproject.forms import TaoTaiLieu

class MonHocListView(ListView, ModelFormMixin):
    model = MonHoc
    template_name = 'dashboard.html'
    paginate_by = 2


def dashboard_view(request):
    ic(request.user.username)
    
    if request.method == 'POST':
        form = ThemMonHoc(request.POST)
        if form.is_valid():
            form.save()
    else:
        # ic(request.GET['p'])
        form = ThemMonHoc()
        # data = MonHoc.objects.all()
        p = Paginator(MonHoc.objects.all(),3)
        page = request.GET.get('page')
        monhoc = p.get_page(page)

    return render(
        request,
        'dashboard.html', 
        {
            'form': form , 
            'monhoc':monhoc
        }
    )

def DuyetTL_view(request):
    return render(
        request,
        'db_DuyetTL.html',
    )

def DongGopTL_view(request):
    if request.method == 'POST':
        form = ThemTaiLieu(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ThemTaiLieu()
    return render(
        request,
        'db_DongGopTL.html', {'form': form}
    )

def TaiLieu_view(request):
    return render(
        request,
        'db_TaiLieu.html',
    )
def ThanhVien_view(request):
    return render(
        request,
        'db_ThanhVien.html',
    )
def BinhLuan_view(request):
    return render(
        request,
        'db_BinhLuan.html',
    )

# def DangTaiLieu(request):
#     if request.method == 'POST':
#         form = TaoTaiLieu(request.POST)
#         form.save()
#         if form.is_valid():
#             instance = form.save()
#             instance.birth_place ='HCM'
#             instance.save()
#             # ok_url = reversed('new_student_form_ok')
#             # return redirect('new_student_form_ok.html')
#     else:
#         form = TaoTaiLieu

#     return render(
#         request,
#         'new_student_form.html',
#         {
#             'form':form,
#         }
#     )