from django.contrib import admin
from .models import Category, Brand, Tag, Product, ProductImage

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # how many empty image upload slots to show by default


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock_quantity', 'category', 'brand', 'seller', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'category', 'brand')
    search_fields = ('name', 'sku', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)  # nicer widget for ManyToMany selection
    inlines = [ProductImageInline]