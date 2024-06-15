from django.contrib import admin
from .models import Categories,SubCategories,Product,Cart,Wishlist,Address,Orders

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name","categories"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name","desc","categories","subcategories","price","image"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["product","quantity","user"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["product","user"]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["address","pincode","user"]


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["order_id","product","quantity","user","order_date","address","payment_status"]