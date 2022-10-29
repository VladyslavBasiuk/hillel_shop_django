from django.contrib import admin
from django.utils.safestring import mark_safe
from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('show_product_image', 'name', 'price', 'sku', 'stock',
                    'available', 'created_at'
                    )
    list_filter = ('name', 'created_at', 'price', 'sku', 'available')
    list_editable = ['name', 'price', 'stock', 'sku', 'available']

    @staticmethod
    def show_product_image(obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="96" height="64" />'.format(
                    obj.image.url)))
        return ''


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('show_category_image', 'name', 'description')

    @staticmethod
    def show_category_image(obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="96" height="64" />'.format(
                    obj.image.url)))
        return ''
