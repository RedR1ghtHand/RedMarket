from django.urls import path
from .views import (
    UserRegisterView,
    login_view,
    account_view,
    logout_view,
    account_settings_view,
    account_order_manager_view,
    account_public_profile_view,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path('user/', account_view, name='user'),
    path('logout/', logout_view, name='logout'),
    path('settings/', account_settings_view, name='settings'),
    path('order_management', account_order_manager_view, name='order_manager'),
    path('profile/<str:mc_username>/', account_public_profile_view, name='public_profile'),
]
