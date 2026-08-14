from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Address


class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'mobile_number')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_profile', 'city', 'state', 'is_default')
    list_filter = ('state', 'is_default')
    search_fields = ('full_name', 'phone', 'city', 'pincode')