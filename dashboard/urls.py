"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from dashboard import views
from django.conf import Settings, settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name='home'),
    path('home/', views.home,name='home'),
    path('login/', views.api_login,name='api_login'),
    path('account_info/', views.account_info,name='account_info'),
    path('api_token_info/',views.api_token_info,name='api_token_info'),
    path('license_detail/', views.license_detail, name='license_detail'),
    path('calldetail_dashboard/', views.PerformanceDashboard, name='PerformanceDashboard'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('standard_user/', views.standard_user, name='standard_user'),
    path('data_export_csv/',views.data_export_csv,name='data_export_csv'),
    path('calldetailrecord/', views.calldetailrecord,name='calldetailrecord'),
    path('bulkdownload_calls/', views.bulkdownload_calls,name='bulkdownload_calls'),
    path('smsListUser/',views.smsUser_list_view,name="smsUser_list_view"),
    path('smsUserCreate/',views.smsUser_create_view,name="smsUser_create_view"),
    path('update/<int:id>',views.smsUser_update_view,name="smsUser_update_view"),
    path('delete/<int:id>',views.smsUser_delete_view,name="smsUser_delete_view"),
    path('sendsms/<int:id>',views.SendSMS,name="SendSMS")

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    