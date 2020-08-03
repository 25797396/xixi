from django.urls import path
from scenic import views

urlpatterns = [
    path('/detail/<int:scenic_id>', views.get_scenic_detail_page)


]