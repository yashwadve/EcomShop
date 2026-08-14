from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('place/', views.place_order, name='place_order'),
    path('', views.order_list, name='my_orders'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]