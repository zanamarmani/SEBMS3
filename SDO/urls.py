from django.urls import path, include
from .import views
from .utills import line_chart, bill_progress_view

from users.views import UserUpdateView, UserDeleteView, update_password,success_page

from django.contrib.auth import views as auth_views

app_name = 'SDO'
urlpatterns = [
    path('', views.dashboard, name='dashboard' ),
    path('create_office_staff/', views.create_office_staff, name='create_office_staff'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('approve_new_consumers/', views.approve_new_consumers, name='approve_new_consumers'),
    path('reject_new_consumers/', views.reject_new_consumers, name='reject_new_consumers'),
    path('add_user/', views.create_user, name='add_user'),
    path('show_all_consumers/', views.show_all_consumers, name='show_all_consumers'),
    path('consumer/<int:consumer_id>/', views.consumer_profile, name='consumer_profile'),
    path('show_all_users/', views.show_all_users, name='show_all_users'),
    path('tariff_list/', views.tariff_list, name='tariff_list'),
    path('update-tariff/', views.create_or_update_tariff, name='update_tariff'),
    path('all_bills/', views.all_bills ,name='all_bills'),
    path('paid_bills/', views.paid_bills, name='paid_bills'),
    path('unpaid_bills/', views.unpaid_bills, name='unpaid_bills'),
    path('line_chart_data/', line_chart, name='line_chart_data'),
    path('bill-progress/', bill_progress_view, name='bill_progress'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/update-password/<int:pk>/', update_password, name='update_password'),
    path('success_page/', success_page,name='success_page'),
    path('sdo/profile/', views.sdo_profile_view, name='sdo_profile'),
    path('sdo/profile/edit/', views.edit_sdo_profile_view, name='edit_sdo_profile'),
    path('sdo/profile/create/', views.create_sdo_profile_view, name='create_sdo_profile'),
   
]

