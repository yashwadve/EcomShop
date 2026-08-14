from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'thumbnail_url', 'unit_price', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'order_status', 'payment_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('order_number', 'razorpay_order_id', 'razorpay_payment_id', 'created_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'order_number', 'total_amount', 'order_status', 'payment_status')
        }),
        ('Shipping Details', {
            'fields': (
                'shipping_full_name', 'shipping_phone',
                'shipping_address_line1', 'shipping_address_line2',
                'shipping_city', 'shipping_state', 'shipping_pincode',
            )
        }),
        ('Payment Gateway Info', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'unit_price', 'quantity', 'subtotal')
    search_fields = ('order__order_number', 'product_name')