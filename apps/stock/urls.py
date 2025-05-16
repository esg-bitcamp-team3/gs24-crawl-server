from django.urls import path

from apps.stock.views.stock import StockView

urlpatterns = [
  path('stock', StockView.as_view(), name='stock'),
]