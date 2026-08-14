from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html', authentication_form=StyledAuthenticationForm,
        ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='catalog:home'), name='logout'),

    path('profile/', views.profile_view, name='my_profile'),

    path('addresses/', views.addresses_view, name='my_addresses'),
    path('addresses/<int:address_id>/edit/', views.edit_address_view, name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address_view, name='delete_address'),
]