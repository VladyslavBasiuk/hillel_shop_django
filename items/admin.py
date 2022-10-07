from django.contrib import admin
from django.utils.safestring import mark_safe
from items.models import Product, Category, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('show_item_image', 'name', 'created_at')
    list_filter = ('created_at',)

    @staticmethod
    def show_item_image(obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ('name', 'price', 'sku')
    list_filter = ('price',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('show_category_image', 'name',)

    @staticmethod
    def show_category_image(obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''
