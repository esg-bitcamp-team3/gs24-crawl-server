from django.urls import path

from apps.crawl.views.news import CompanyNewsView

urlpatterns = [
  path('company', CompanyNewsView.as_view(), name='company-news'),
]