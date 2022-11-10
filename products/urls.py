from django.contrib.auth.decorators import login_required
from django.urls import path
from products.views import ProductView, export_csv, ImportCSV, \
    ProductDetailView, FavoriteProductsView, FavoriteProductAddOrRemoveView

urlpatterns = [
    path('products', ProductView.as_view(), name='products'),
    path('products/export_csv', export_csv, name='export_csv'),
    path('products/import_csv', ImportCSV.as_view(), name='import_csv'),
    path('products/<uuid:pk>', ProductDetailView.as_view(),
         name='product_detail'),
    path('favorites/',
         login_required(FavoriteProductsView.as_view()),
         name='favorites'),
    path('favorites/<uuid:pk>/',
         login_required(FavoriteProductAddOrRemoveView.as_view()),
         name='add_or_remove_favorite'),
]
