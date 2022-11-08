import decimal
from django.db import models
from shop.constans import DECIMAL_PLACES, MAX_DIGITS
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


class CurrencyHistory(PKMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    def __str__(self):
        return f'{self.currency} | {self.created_at} |{self.buy} | {self.sale}'

    @classmethod
    def last_curs(cls, currency_code, attr='sale') -> decimal.Decimal:
        """

        :param currency_code: ccy or iso code currency
        :param attr: currency USD [sale]
        :return: last created curs currency
        """
        return getattr(cls.objects.filter(
            currency=currency_code
        ).order_by(
            '-created_at'
        ).first(), attr, decimal.Decimal('1.00'))
