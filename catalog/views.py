from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand
from reviews.forms import ReviewForm
from orders.models import Order
from reviews.models import Review
from django.core.paginator import Paginator


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]

    return render(request, 'catalog/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {
        'page_obj': page_obj,
        'categories': Category.objects.filter(is_active=True),
        'brands': Brand.objects.filter(is_active=True),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.filter(status='approved').select_related('user').order_by('-created_at')

    can_review = False
    already_reviewed = False

    if request.user.is_authenticated:
        order = Order.objects.filter(
            user=request.user,
            payment_status='paid',
            items__product=product,
        ).order_by('-created_at').first()

        if order:
            if Review.objects.filter(product=product, order=order).exists():
                already_reviewed = True
            else:
                can_review = True

    review_form = ReviewForm()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'can_review': can_review,
        'already_reviewed': already_reviewed,
        'review_form': review_form,
    })


def search_results(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True, name__icontains=query) if query else Product.objects.none()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/search_results.html', {
        'page_obj': page_obj,
        'query': query,
        'result_count': paginator.count,
    })