from django.urls import path
from . import views

urlpatterns = [
    path('/index', views.get_hotel_index_page),
    path('/info', views.get_hotel_info),
    path('/detail', views.get_hotel_detail_page),
    path('/order/<str:user>', views.HotelOrderView.as_view()),
]