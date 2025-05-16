from django.urls import path

from apps.stock.views.financial_data import FinancialDataView
from apps.stock.views.stock import StockView

urlpatterns = [
  path('stock', StockView.as_view(), name='stock'),
  path('financial-data', FinancialDataView.as_view(), name='financial-data'),
]