from django.contrib import admin
from products.models import *


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')
    list_filter = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'price', 'created_at', 'updated_at')
    list_filter = ('product_name', 'product_category', 'price', )
    search_fields = ('product_name', 'product_category', 'price',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Product, ProductAdmin)

class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'order_status', 'created_at', 'updated_at')
    list_filter = ('user', 'product', 'quantity', 'total_price', 'order_status', )
    search_fields = ('user', 'product', 'quantity', 'total_price', 'order_status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ProductOrder, ProductOrderAdmin)


class ProductCheckoutAdmin(admin.ModelAdmin):
    list_display = ('product_order', 'payment_status', 'payment_method', 'created_at', 'updated_at')
    list_filter = ('product_order', 'payment_status', )
    search_fields = ('product_order', 'payment_status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ProductCheckout, ProductCheckoutAdmin)


class ProductShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('product_checkout', 'address', 'city', 'state', 'zip_code', 'created_at', 'updated_at')
    list_filter = ('product_checkout', 'address', 'city', 'state', 'zip_code', )
    search_fields = ('product_checkout', 'address', 'city', 'state', 'zip_code',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ProductShippingAddress, ProductShippingAddressAdmin)

# Register your models here.
