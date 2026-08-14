from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalog.models import Product
from .models import Cart, CartItem


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    total = sum(item.subtotal() for item in items)

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))
    buy_now = request.POST.get('action') == 'buy_now'

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        quantity = cart_item.quantity + quantity

    if quantity > product.stock_quantity:
        messages.error(request, f'Only {product.stock_quantity} unit(s) of "{product.name}" available in stock.')
        if created:
            cart_item.delete()
        return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))

    cart_item.quantity = quantity
    cart_item.save()

    if buy_now:
        return redirect('orders:checkout')

    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'catalog:home'))


@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        new_quantity = int(request.POST.get('quantity', cart_item.quantity))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
        return redirect('cart:view_cart')

    if new_quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    elif new_quantity > cart_item.product.stock_quantity:
        messages.error(request, f'Only {cart_item.product.stock_quantity} unit(s) available.')
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('cart:view_cart')


@login_required
@require_POST
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:view_cart')