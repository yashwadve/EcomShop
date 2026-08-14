from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalog.models import Product
from orders.models import Order
from .models import Review
from .forms import ReviewForm


@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Verified purchase check: find the user's most recent PAID order containing this product
    order = (
        Order.objects.filter(
            user=request.user,
            payment_status='paid',
            items__product=product,
        )
        .order_by('-created_at')
        .first()
    )

    if not order:
        messages.error(request, 'You can only review products you have purchased and paid for.')
        return redirect('catalog:product_detail', slug=product.slug)

    if Review.objects.filter(product=product, order=order).exists():
        messages.error(request, 'You have already reviewed this product for this order.')
        return redirect('catalog:product_detail', slug=product.slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.order = order
        review.status = 'pending'
        review.save()
        messages.success(request, 'Review submitted! It will appear after admin approval.')
    else:
        messages.error(request, 'Please provide a valid rating and comment.')

    return redirect('catalog:product_detail', slug=product.slug)