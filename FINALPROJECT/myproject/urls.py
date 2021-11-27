from django.urls import path
from myproject import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     # path('Toan_Tin_KHTN',views.Toan_Tin_KHTN,name='Toan_Tin_KHTN'),
     # path('slide',views.SlideListview.as_view(),name='slide'),
     # path('DeThi',views.DeThiListview.as_view(),name='DeThi'),
     # path('BaiTap',views.BaiTapListview.as_view(),name='BaiTap'),

     # path('mon_cu_the',views.mon_cu_the,name='mon_cu_the'),
     # path('downloadfile',views.downloadfile,name='downloadfile'),

     # path('', views.home_view, name='home'),
     path('ERROR',views.error, name="error"),
     path("subjects/<slug:MaMH>/",views.MonHoc_show, name=""),
     path("subjects/<slug:MaMH>/<slug:LoaiTL>/",views.MonHoc_LoaiTL_show, name="MonHoc_LoaiTL_show"),
     path('category/<slug:NhomMH>/<slug:Khoa>/',views.MonHocList_view),
     path('document/<slug:slug>/',views.one_document_view),     
     path('thongbao/<slug:slug>/read',views.Doc_Thong_Bao),

     path('dashboard/', views.dashboard_view, name='dashboard_view'),
     path('dashboard/DuyetTL/', views.DuyetTL_view, name='DuyetTL_view'),
     path('dashboard/DuyetTL/Preview/<slug:MaTL>', views.TaiLieu_Preview, name='TaiLieu_Preview'),
     path('dashboard/DuyetTL/XetDuyet/<slug:slug>', views.TaiLieu_Duyet, name='TaiLieu_Duyet'),
     path('dashboard/DongGopTL/', views.DongGopTL_view, name='DongGopTL_view'),
     path('dashboard/TaiLieu/', views.TaiLieu_view, name='TaiLieu_view'),
     path('dashboard/TaiLieu/delete/<slug:slug>', views.TaiLieu_delete, name='TaiLieu_delete'),
     path('dashboard/ThanhVien/', views.ThanhVien_view, name='ThanhVien_view'),
     path('dashboard/ThanhVien/Active/<slug:username>', views.ThanhVien_Active, name='ThanhVien_Active'),
     path('dashboard/ThanhVien/Staff/<slug:username>', views.ThanhVien_Staff, name='ThanhVien_Staff'),
     path('dashboard/BinhLuan/', views.BinhLuan_view, name='BinhLuan_view'),
     path('ThongTinCaNhan/', views.ThongTinCaNhan_view, name='ThongTinCaNhan_view'),

     path('DangKy/', views.DangKy_view, name='DangKy_view'),
     path('', views.home_view, name='home_view'),
     path('DangNhap/', auth_views.LoginView.as_view(template_name='global_DangNhap.html'),name='DangNhap_view'),
     path('DangXuat/', auth_views.LogoutView.as_view(next_page='/'),name='DangXuat_view'),
     path('search/', views.search_view, name='search'),

     
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


