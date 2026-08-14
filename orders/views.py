import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.core.paginator import Paginator


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')

    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view_cart')

    profile = getattr(request.user, 'profile', None)
    addresses = profile.addresses.all() if profile else []

    if not addresses:
        messages.error(request, 'Please add a shipping address before checkout.')
        return redirect('accounts:my_addresses')

    default_address = addresses.filter(is_default=True).first()
    total = sum(item.subtotal() for item in items)
    form = CheckoutForm(user=request.user, initial={'address': default_address.id if default_address else None})

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total,
        'form': form,
        'addresses': addresses,
    })


@login_required
@require_POST
def place_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')

    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view_cart')

    form = CheckoutForm(request.POST, user=request.user)
    if not form.is_valid():
        messages.error(request, 'Please select a valid shipping address.')
        return redirect('orders:checkout')

    address = form.cleaned_data['address']

    # Validate stock for every item before committing anything
    for item in items:
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f'"{item.product.name}" only has {item.product.stock_quantity} unit(s) in stock.')
            return redirect('cart:view_cart')

    total_amount = sum(item.subtotal() for item in items)
    order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=total_amount,
            order_status='created',
            payment_status='pending',
            shipping_full_name=address.full_name,
            shipping_phone=address.phone,
            shipping_address_line1=address.address_line1,
            shipping_address_line2=address.address_line2,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_pincode=address.pincode,
        )

        for item in items:
            product = item.product
            first_image = product.images.first()

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                thumbnail_url=first_image.image.url if first_image else '',
                unit_price=product.price,
                quantity=item.quantity,
                subtotal=item.subtotal(),
            )

            product.stock_quantity -= item.quantity
            product.save()

        items.delete()  

    messages.success(request, f'Order {order.order_number} placed successfully!')
    return redirect('payments:create_order', order_id=order.id)   


@login_required
def order_list(request):
    orders_qs = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/order_list.html', {'page_obj': page_obj})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})