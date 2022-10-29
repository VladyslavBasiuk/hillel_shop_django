from django.urls import path
from products.views import ProductView, export_csv, ImportCSV, ProductDetail

urlpatterns = [
    path('products', ProductView.as_view(), name='products'),
    path('products/export_csv', export_csv, name='export_csv'),
    path('products/import_csv', ImportCSV.as_view(), name='import_csv'),
    path('products/<uuid:pk>', ProductDetail.as_view(), name='product_detail'),
]
