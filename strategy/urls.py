from django.urls import path
from . import views

urlpatterns = [
    path('/writestrategy', views.get_writestrategy_page),
    path('/strategy/<str:user>', views.StrategyView.as_view()),
    path('/<str:user>/detail', views.get_detail_page),
    path('/upload', views.upload),
    path('/<str:user>/message', views.Message.as_view()),
    path('', views.get_strategyindex_page),
    path('/<str:user>', views.get_strategy_page),
]
