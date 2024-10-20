
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from users.views import success_page
app_name = 'officestaff'
urlpatterns = [
    path('',views.Home, name = 'home'),
    path('registerconsumer/', views.register_consumer, name='registerconsumer'),
    path('consumers/', views.list_consumers, name='list_consumers'),
    path('all_readings_from_firebase/', views.Get_All_Readings, name='all_readings_from_firebase'),
    path('all_readings/', views.all_readings, name='all_readings'),
    path('generate-bill/<str:meter_number>/', views.generate_bill, name='generate_bill'),
    path('save_meter_data/', views.save_meter_data_to_db, name='save_meter_data'),
    path('all_bills/', views.all_bills ,name='all_bills'),
    path('paid_bills/', views.paid_bills, name='paid_bills'),
    path('unpaid_bills/', views.unpaid_bills, name='unpaid_bills'),
    path('generate_bills/', views.Generate_bill, name='generate_bills'),
    path('show_profile/', views.show_profile, name='show_profile'),
    path('success/', success_page, name='success_page'),
    path('consumer/delete/<int:pk>/', views.delete_unapproved_consumer, name='delete_unapproved_consumer'),
    path('assign-meter/', views.assign_meter_view, name='assign_meter'),

]
