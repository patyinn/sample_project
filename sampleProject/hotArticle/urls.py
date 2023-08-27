from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from hotArticle import views

app_name = 'hot_article'

urlpatterns = [
    path('', views.HotArticleView.as_view(), name='HotArticle'),
    path('<str:pk>/', views.HotArticleDetailView.as_view(), name='HotArticleDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)