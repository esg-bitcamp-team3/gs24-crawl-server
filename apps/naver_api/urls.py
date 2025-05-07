from django.urls import path

from apps.naver_api.views.search_news import SearchNewsView

urlpatterns = [
  path('news', SearchNewsView.as_view(), name='news'),
]