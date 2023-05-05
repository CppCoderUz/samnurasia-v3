


from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('team', views.team_views, name='team'),
    path('arxiv', views.arxiv, name='arxiv'),
    path('news', views.news, name='news'),
    path('news/<int:pk>', views.news, name='news_detail'),
    path('journal/<int:pk>', views.detail_journal, name='detail_journal'),
    path('col/<int:pk>', views.detail_col, name='detail_col'),
]
