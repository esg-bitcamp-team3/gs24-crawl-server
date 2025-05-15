from django.urls import path

from apps.market_price.views.carbon_price import CarbonPriceView
from apps.market_price.views.exchange_rate import ExchangeRateView

urlpatterns = [
  path('carbon-price', CarbonPriceView.as_view(), name='carbon_price'),
  path('exchage-rate', ExchangeRateView.as_view(), name='exchange_rate'),
]