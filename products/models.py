from os import path
from django.db import models
from shop.constans import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency
from django.core.cache import cache


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}' \
           f'{instance.pk}/image{extension}'


class Product(PKMixin):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image,
                              default='static/images/example_img.jpg'
                              )
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    products = models.ManyToManyField('products.Product', blank=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )

    @classmethod
    def _cache_key(cls):
        return 'products'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._cache_key())
        if not products:
            products = Product.objects.all()
            cache.set(cls._cache_key(), products)
        return products

    def __str__(self):
        return f'{self.name} | {self.category} | {self.price} | {self.sku} | {self.stock}' # noqa


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return f'{self.name} | {self.description}'
