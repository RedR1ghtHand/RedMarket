from django.urls import path
from .views import UserRegisterView, login_view, account_view, logout_view

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path('user/', account_view, name='user'),
    path('logout/', logout_view, name='logout')
]
