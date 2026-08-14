import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import User
from catalog.models import Category, Brand, Tag, Product, ProductImage


CATEGORIES = ["Electronics", "Watches", "Footwear", "Beverages", "Bags", "Computer Accessories"]
BRANDS = ["Fossil", "Logitech", "Dell", "Bisleri", "Adidas", "Sony"]
TAGS = ["new", "trending", "bestseller", "sale", "premium"]

PRODUCTS = [
    {"name": "Fossil Gen 6 Smartwatch", "category": "Watches", "brand": "Fossil",
     "price": 2588, "sku": "FOS-GEN6-BLKSTL", "desc": "Fossil Gen 6 Smartwatch with AMOLED display and advanced health tracking.",
     "short": "AMOLED display and advanced health tracking.", "tags": ["new", "trending"], "featured": True},

    {"name": "Logitech M235 Wireless Mouse", "category": "Computer Accessories", "brand": "Logitech",
     "price": 855, "sku": "LOG-M235-WL", "desc": "Compact wireless mouse with smooth tracking and long battery life.",
     "short": "Compact wireless mouse with smooth tracking.", "tags": ["bestseller"], "featured": True},

    {"name": "Bisleri Mineral Water Bottle 1L", "category": "Beverages", "brand": "Bisleri",
     "price": 20, "sku": "BIS-1L-MIN", "desc": "Pure and safe drinking water enriched with minerals, available in a 1-litre bottle.",
     "short": "Pure and safe drinking water enriched with minerals.", "tags": ["bestseller"], "featured": False},

    {"name": "Dell XPS 15 (2025 Edition)", "category": "Electronics", "brand": "Dell",
     "price": 98555, "sku": "DEL-XPS15-25", "desc": "Dell XPS 15 2025 with Intel Core Ultra processor and stunning InfinityEdge display.",
     "short": "Intel Core Ultra processor, InfinityEdge display.", "tags": ["premium", "new"], "featured": True},

    {"name": "Adidas Classic School Backpack", "category": "Bags", "brand": "Adidas",
     "price": 1299, "sku": "ADI-BKPK-CLS", "desc": "Durable everyday backpack with padded straps and multiple compartments.",
     "short": "Durable everyday backpack.", "tags": ["sale"], "featured": False},

    {"name": "Sony WH-1000XM5 Wireless Headphones", "category": "Electronics", "brand": "Sony",
     "price": 24990, "sku": "SNY-WH1000XM5", "desc": "Industry-leading noise cancellation with premium sound quality.",
     "short": "Industry-leading noise cancellation.", "tags": ["premium", "bestseller"], "featured": True},

    {"name": "Nilkamal Mid Back Office Chair", "category": "Electronics", "brand": "Dell",
     "price": 4999, "sku": "NIL-MIDBACK-01", "desc": "Ergonomic mid-back office chair with lumbar support.",
     "short": "Ergonomic mid-back office chair.", "tags": ["sale"], "featured": False},

    {"name": "Fossil Classic Leather Wallet", "category": "Bags", "brand": "Fossil",
     "price": 1899, "sku": "FOS-WLT-LTHR", "desc": "Genuine leather bifold wallet with RFID protection.",
     "short": "Genuine leather bifold wallet.", "tags": ["new"], "featured": False},
]


class Command(BaseCommand):
    help = "Seeds the database with dummy categories, brands, tags, products, and downloaded placeholder images."

    def handle(self, *args, **options):
        # Get or create a seller user to own the products
        seller, created = User.objects.get_or_create(
            username="demo_seller",
            defaults={"email": "seller@example.com", "role": "seller"},
        )
        if created:
            seller.set_password("testpass123")
            seller.save()
            self.stdout.write(self.style.SUCCESS("Created demo_seller (password: testpass123)"))

        # Categories
        category_map = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            category_map[name] = cat

        # Brands
        brand_map = {}
        for name in BRANDS:
            brand, _ = Brand.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            brand_map[name] = brand

        # Tags
        tag_map = {}
        for name in TAGS:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_map[name] = tag

        # Products
        for data in PRODUCTS:
            product, created = Product.objects.get_or_create(
                sku=data["sku"],
                defaults={
                    "name": data["name"],
                    "slug": slugify(data["name"]),
                    "short_description": data["short"],
                    "description": data["desc"],
                    "price": data["price"],
                    "stock_quantity": 25,
                    "category": category_map[data["category"]],
                    "brand": brand_map[data["brand"]],
                    "seller": seller,
                    "is_active": True,
                    "is_featured": data["featured"],
                },
            )
            if created:
                product.tags.set([tag_map[t] for t in data["tags"]])
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))

                # Download 2 placeholder images per product using picsum.photos (seeded = consistent per product)
                for i in range(2):
                    seed = f"{data['sku']}-{i}"
                    url = f"https://picsum.photos/seed/{seed}/600/600"
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            img = ProductImage(product=product)
                            img.image.save(f"{data['sku']}_{i}.jpg", ContentFile(response.content), save=True)
                            self.stdout.write(f"  -> downloaded image {i+1}")
                    except requests.RequestException as e:
                        self.stdout.write(self.style.WARNING(f"  -> failed to download image: {e}"))
            else:
                self.stdout.write(f"Skipped (already exists): {product.name}")

        self.stdout.write(self.style.SUCCESS("\nSeeding complete!"))