import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from orders.models import Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def create_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_status == 'paid':
        messages.info(request, 'This order is already paid.')
        return redirect('orders:order_detail', order_id=order.id)

    # Razorpay expects amount in paise (smallest currency unit), so multiply by 100
    amount_paise = int(order.total_amount * 100)

    razorpay_order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': order.order_number,
        'payment_capture': 1,
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        'order': order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount_paise': amount_paise,
    }
    return render(request, 'payments/checkout_payment.html', context)


@csrf_exempt
@require_POST
def verify_payment(request):
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        })
    except razorpay.errors.SignatureVerificationError:
        order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
        if order:
            order.payment_status = 'failed'
            order.save()
            return JsonResponse({'status': 'failed', 'redirect_url': f'/payments/failed/{order.id}/'})
        return JsonResponse({'status': 'failed'}, status=400)

    order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
    order.razorpay_payment_id = razorpay_payment_id
    order.payment_status = 'paid'
    order.order_status = 'paid'
    order.save()

    return JsonResponse({'status': 'success', 'redirect_url': f'/orders/{order.id}/'})


@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.payment_status != 'paid':
        order.payment_status = 'failed'
        order.save()
    return render(request, 'payments/payment_failed.html', {'order': order})