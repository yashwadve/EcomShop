from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('cart__user__username', 'product__name')