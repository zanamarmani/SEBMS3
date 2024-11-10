from django.urls import path, include
from .import views
from .utills import line_chart, bill_progress_view

from users.views import UserUpdateView, UserDeleteView, update_password,success_page

from django.contrib.auth import views as auth_views
from . import utills
app_name = 'SDO'
urlpatterns = [
    path('', views.dashboard, name='dashboard' ),
    path('create_office_staff/', views.create_office_staff, name='create_office_staff'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('approve_new_consumers/', views.approve_new_consumers, name='approve_new_consumers'),
    path('reject_new_consumers/', views.reject_new_consumers, name='reject_new_consumers'),
    path('add_user/', views.create_user, name='add_user'),
    path('show_all_consumers/', views.show_all_consumers, name='show_all_consumers'),
    path('print_all_consumers/', views.print_all_consumers, name='print_all_consumers'),
    path('consumer_delete/<int:pk>/', views.delete_consumer, name='delete_consumer'),
    path('consumer/<int:consumer_id>/', views.consumer_profile, name='consumer_profile'),
    path('show_all_users/', views.show_all_users, name='show_all_users'),
    path('tariff_list/', views.tariff_list, name='tariff_list'),
    path('update-tariff/', views.create_or_update_tariff, name='update_tariff'),
    path('all_bills/', views.all_bills ,name='all_bills'),
    path('print_all_bills/', views.print_all_bills ,name='print_all_bills'),
    path('paid_bills/', views.paid_bills, name='paid_bills'),
    path('unpaid_bills/', views.unpaid_bills, name='unpaid_bills'),
    path('line-chart-data/', utills.line_chart, name='line_chart'),
    path('bill-progress/', bill_progress_view, name='bill_progress'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/update-password/<int:pk>/', update_password, name='update_password'),
    path('success_page/', success_page,name='success_page'),
    path('sdo/profile/', views.sdo_profile_view, name='sdo_profile'),
    path('sdo/profile/edit/', views.edit_sdo_profile_view, name='edit_sdo_profile'),
    path('sdo/profile/create/', views.create_sdo_profile_view, name='create_sdo_profile'),
    path('sdo_dashboard/payment_data/', utills.payment_data, name='payment_data'),
    path('monthly_report/', views.generate_monthly_report, name='monthly_report'),
    path('transactions/', views.payment_transactions, name='payment_transactions'),
    path('transactions/print/', views.print_payment_transactions, name='print_transactions'),

    path('transactions/pdf/', views.transactions_pdf, name='transactions_pdf'),
    path('bills/pdf/<str:month>/<str:paid>/', views.bills_pdf, name='bills_pdf'),
    path('consumers/pdf/<str:division>/', views.consumers_pdf, name='consumers_pdf'),
]

