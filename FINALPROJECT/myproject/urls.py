from django.urls import path


from myproject import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('dashboard/a/', views.MonHocListView.as_view(), name='dashboard_view2'),
    path('dashboard/DuyetTL/', views.DuyetTL_view, name='DuyetTL_view'),
    path('dashboard/DongGopTL/', views.DongGopTL_view, name='DongGopTL_view'),
    path('dashboard/TaiLieu/', views.TaiLieu_view, name='TaiLieu_view'),
    path('dashboard/TaiLieu/delete/<slug:slug>', views.TaiLieu_delete, name='TaiLieu_delete'),
    path('dashboard/ThanhVien/', views.ThanhVien_view, name='ThanhVien_view'),
    path('dashboard/BinhLuan/', views.BinhLuan_view, name='BinhLuan_view'),
    path('DangKy/', views.DangKy_view, name='DangKy_view'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),
    
]
