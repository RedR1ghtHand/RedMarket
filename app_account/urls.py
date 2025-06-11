from django.urls import path, include
from .views import (
    UserRegisterView,
    login_view,
    account_view,
    logout_view,
    account_settings_view,
    AccountOrderManagerView,
    PublicProfileView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path('user/', account_view, name='user'),
    path('logout/', logout_view, name='logout'),
    path('settings/', account_settings_view, name='settings'),
    path('order_management', AccountOrderManagerView.as_view(), name='order_manager'),
    path('profile/<str:mc_username>/', PublicProfileView.as_view(), name='public_profile'),
    path('', include("app_social.urls"))
]
