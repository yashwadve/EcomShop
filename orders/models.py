from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=30, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    shipping_full_name = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=15)
    shipping_address_line1 = models.CharField(max_length=200)
    shipping_address_line2 = models.CharField(max_length=200, blank=True, null=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=50)
    shipping_pincode = models.CharField(max_length=10)

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)     # snapshot
    thumbnail_url = models.CharField(max_length=300, blank=True, null=True)  # snapshot
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)        # snapshot
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"