from django.urls import path
from . import views

app_name = 'consumer'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('bill_history/', views.bill_history, name='bill_history'),
    path('current_bill/', views.current_bill, name='current_bill'),
    path('print_current_bill/', views.print_current_bill, name='print_current_bill'),
    path('pay_bills_now/', views.pay_bills_now, name='pay_bills_now'),
    path('pay_bill_demo/', views.pay_bill_demo, name='pay_bill_demo'),

]