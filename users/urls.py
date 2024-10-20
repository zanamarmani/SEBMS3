from django.urls import path,include
from . import views
from SDO.views import show_all_users
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('login/', views.user_login, name='login'),
    path('sdo_dashboard/', include('SDO.urls')),
    path('office_staff/', include('officestaff.urls')),
    path('meter_reader/', include('meterreader.urls')),
    path('consumer/', include('consumer.urls')),
    path('payment/', include('payment.urls')),
    path('show_all_users/',show_all_users, name='show_all_users'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('success_page/', views.success_page,name='success_page'),
    
]
