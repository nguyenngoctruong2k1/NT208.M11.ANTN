from django.urls import path
from myproject import views

urlpatterns = [
    path('', views.home_view, name='home'),
    #path('one_document', views.one_document_view, name='one_document'),
    #path('mon_cu_the',views.mon_cu_the,name='mon_cu_the'),
    path('Toan_Tin_KHTN',views.Toan_Tin_KHTN,name='Toan_Tin_KHTN'),
    #path('slide',views.Slide,name='slide'),
    path('slide',views.SlideListview.as_view(),name='slide'),
    #path('DeThi',views.DeThi,name='DeThi'),
    path('DeThi',views.DeThiListview.as_view(),name='DeThi'),
    #path('BaiTap',views.BaiTap,name='BaiTap'),
    path('BaiTap',views.BaiTapListview.as_view(),name='BaiTap'),
    path('<int:MaTL>/',views.one_document_view),
    #path('LoaiTL',views.slide_DeThi_BaiTap)
    path('<int:MaMH>/',views.comment, name='mon_cu_the')
]



