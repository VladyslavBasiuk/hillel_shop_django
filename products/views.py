import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import OuterRef, Exists
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView
from products.forms import ImportForm
from products.models import Product, FavoriteProduct
from shop.mixins.views_mixins import UserVerification
from shop.settings import DOMAIN


class ProductView(ListView):
    model = Product

    def get_queryset(self):
        qs = self.model.get_products()
        if self.request.user.is_authenticated:
            sq = FavoriteProduct.objects.filter(
                product=OuterRef('id'),
                user=self.request.user
            )
            qs = qs \
                .prefetch_related('in_favorites') \
                .annotate(is_favorite=Exists(sq))
        return qs


class ProductDetailView(DetailView):
    model = Product


class FavoriteProductsView(ListView):
    model = FavoriteProduct

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('product', 'user', 'product__category')\
            .prefetch_related('product__products')
        return qs


class FavoriteProductAddOrRemoveView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        """
        Get or create favorite list. Is not create - remove from favorites.
        :param request: user (is_authenticated?)
        :param args:
        :param kwargs:
        :return: Go to the Products page.
        """
        product = self.get_object()
        user = request.user
        favorite, created = FavoriteProduct.objects.get_or_create(
            product=product,
            user=user
        )
        messages.success(request, message='Product was add to favourites!')
        if not created:
            favorite.delete()
            messages.warning(request, message='Product was deleted!')
        return HttpResponseRedirect(reverse_lazy('products'))


@login_required
def export_csv(request, *args, **kwargs):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="products.csv"'}
    )
    fieldnames = ['name', 'category', 'description', 'price', 'sku', 'image']
    writer = csv.DictWriter(response, fieldnames=fieldnames)

    writer.writeheader()
    for product in Product.objects.iterator():
        writer.writerow({
            'name': product.name,
            'category': product.category.name,
            'description': product.description,
            'price': product.price,
            'sku': product.sku,
            'image': DOMAIN + product.image.url
        })
    return response


class ImportCSV(UserVerification, FormView):
    template_name = 'products/import_csv.html'
    form_class = ImportForm
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
