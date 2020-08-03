from django.urls import path
from user import views

urlpatterns = [
    path('/sms', views.sms_view),
    path('/<str:user>/change_password', views.change_password),
    path('/login', views.loginview),
    path('/index', views.loginandregister),
    path('/register', views.register),
    path('/login_check', views.login),
    path('/info/<str:user>', views.UserInfo.as_view()),
    # path('/change_info/<str:user>', views.ChangeinfoView.as_view()),
    path('/upload_avatar/<str:user>', views.upload_avatar)
]
