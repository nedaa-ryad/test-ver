from django.contrib import admin

from .models import Cart, Customer, Product, ProductImage, Wishlist


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',
    'description', 'category', 'price', 'image', 'discountPrice']

@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'images']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipCode', 'mobile']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'price_id']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']