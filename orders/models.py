from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    BEFORE_SAVE
from shop.constans import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes


class Discount(LifecycleModelMixin, PKMixin):
    amount = models.DecimalField(
        default=0,
        decimal_places=DECIMAL_PLACES,
        max_digits=MAX_DIGITS
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self):
        return f'{self.code} | {self.amount} | {self.is_active}'


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    products = models.ManyToManyField("products.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    def total_amount_with_discount(self):
        if self.discount:
            if self.products.exists():
                if self.discount.discount_type == DiscountTypes.VALUE:
                    return (self.total_amount - self.discount.amount).quantize(
                        Decimal('.00'))
                elif self.discount.discount_type == DiscountTypes.PERCENT:
                    return self.total_amount - (self.total_amount / 100 *
                                                self.discount.amount).quantize(
                        Decimal('.00'))
        return self.total_amount

    def __str__(self):
        return f'{self.total_amount_with_discount()}'

    @hook(BEFORE_SAVE)
    def order_after_save(self):
        self.total_amount = 0
        for product in self.products.all():
            self.total_amount += product.price

    @hook(AFTER_UPDATE)
    def order_after_update(self):
        if self.discount:
            self.total_amount = self.total_amount_with_discount()
            self.save(update_fields=('total_amount',))
