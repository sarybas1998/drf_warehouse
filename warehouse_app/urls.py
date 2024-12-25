from django.urls import path
from warehouse_app.views import CatalogAPIView, ProductDetailAPIView, SearchAPIView, UpdateStocksAPIView


urlpatterns = [
    path('catalog/', CatalogAPIView.as_view(), name='catalog'),
    path('product/<int:product_id>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('catalog/update/stocks', UpdateStocksAPIView.as_view(), name='update_stocks'),
]
