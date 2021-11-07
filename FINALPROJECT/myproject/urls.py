from django.urls import path
from myproject import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('Toan_Tin_KHTN',views.Toan_Tin_KHTN,name='Toan_Tin_KHTN'),
    path('slide',views.SlideListview.as_view(),name='slide'),
    path('DeThi',views.DeThiListview.as_view(),name='DeThi'),
    path('BaiTap',views.BaiTapListview.as_view(),name='BaiTap'),
    
    path('mon_cu_the',views.mon_cu_the,name='mon_cu_the'),
    path("subjects/<slug:MaMH>/",views.MonHoc_show, name=""),
    path('category/<slug:NhomMH>/<slug:Khoa>/',views.MonHocList_view),
    path('document/<slug:slug>/',views.one_document_view),
    path('downloadfile',views.downloadfile,name='downloadfile'),


    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('dashboard/DuyetTL/', views.DuyetTL_view, name='DuyetTL_view'),
    path('dashboard/DongGopTL/', views.DongGopTL_view, name='DongGopTL_view'),
    path('dashboard/TaiLieu/', views.TaiLieu_view, name='TaiLieu_view'),
    path('dashboard/TaiLieu/delete/<slug:slug>', views.TaiLieu_delete, name='TaiLieu_delete'),
    path('dashboard/ThanhVien/', views.ThanhVien_view, name='ThanhVien_view'),
    path('dashboard/BinhLuan/', views.BinhLuan_view, name='BinhLuan_view'),
    path('DangKy/', views.DangKy_view, name='DangKy_view'),
    # path('', views.home_view, name='home_view'),
    path('', views.home_view, name='home_view'),
    path('DangNhap/', auth_views.LoginView.as_view(template_name='login.html'),
         name='DangNhap_view'),
    path('DangXuat/', auth_views.LogoutView.as_view(next_page='/'),
         name='DangXuat_view')
]



