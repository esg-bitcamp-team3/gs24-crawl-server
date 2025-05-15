from django.urls import path

from apps.naver_api.views.search_news import SearchNewsView, KeyWordNewsView
from apps.naver_api.views.sentiment import KoBertSentimentAnalysisView

urlpatterns = [
  path('news', SearchNewsView.as_view(), name='news'),
  path('keyword-news', KeyWordNewsView.as_view(), name='keyword-news'),
  path('sentiment', KoBertSentimentAnalysisView.as_view(), name='sentiment'),
]