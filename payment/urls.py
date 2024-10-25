

from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('pay_online/<int:bill_id>/', views.payment_gateway, name='payment_gateway'),
    path('jazzcash_payment/<int:bill_id>/', views.jazzcash_payment, name='jazzcash_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('success/', views.payment_success, name='payment_success'),
]