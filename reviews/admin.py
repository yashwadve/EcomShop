from django.contrib import admin
from django.utils import timezone
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status', 'created_at', 'approved_by')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('product', 'user', 'order', 'created_at', 'updated_at', 'approved_by', 'approved_at')
    actions = ['approve_reviews', 'reject_reviews']

    fieldsets = (
        ('Review Info', {
            'fields': ('product', 'user', 'order', 'rating', 'comment')
        }),
        ('Moderation', {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(
            status='approved',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} review(s) approved.")

    @admin.action(description='Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(
            status='rejected',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} review(s) rejected.")