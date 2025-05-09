from django.urls import path

from apps.naver_api.views.search_news import SearchNewsView, KeyWordNewsView

urlpatterns = [
  path('news', SearchNewsView.as_view(), name='news'),
  path('keyword-news', KeyWordNewsView.as_view(), name='keyword-news'),
]