from django.urls import path

from apps.market_price.views.carbon_price import CarbonPriceView

urlpatterns = [
  path('carbon-price', CarbonPriceView.as_view(), name='carbon_price'),
]