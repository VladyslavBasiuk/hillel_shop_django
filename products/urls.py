from django.urls import path
from products.views import ProductView, export_csv, ImportCSV

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/export_csv/', export_csv, name='export_csv'),
    path('products/import_csv/', ImportCSV.as_view(),
         name='import_csv')
]
