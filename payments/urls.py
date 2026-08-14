from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<int:order_id>/', views.create_order, name='create_order'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('failed/<int:order_id>/', views.payment_failed, name='payment_failed'),
]