from django.urls import path

from apps.stock.views.financial import SingleCompanyFinancialAPIView
from apps.stock.views.financial_data import FinancialDataView
from apps.stock.views.stock import StockView, StockHistoryView

urlpatterns = [
  path('stock', StockView.as_view(), name='stock'),
  path('stock-history', StockHistoryView.as_view(), name='stock-history'),
  path('financial-data', FinancialDataView.as_view(), name='financial-data'),
  path('single-financial', SingleCompanyFinancialAPIView.as_view(), name='single-financial'),
]