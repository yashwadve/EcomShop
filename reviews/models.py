from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    product = models.ForeignKey('catalog.Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)  # ensures "verified purchase"
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_reviews'
    )
    approved_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'order')

    def __str__(self):
        return f"{self.rating} by {self.user.username} on {self.product.name}"
    
    
    