from django.contrib import admin

from .models import Product, Customer, Category

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_filter = ("date", "categories")
    list_display = ("title", "date")

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)