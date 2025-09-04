from django.urls import include, path

from .views import (
    OrderCardDeleteView,
    OrderCardUpdateView,
    OrderManagerView,
    PublicProfileView,
    UserRegisterView,
    account_settings_view,
    account_view,
    login_view,
    logout_view,
)

urlpatterns = [
    # Authentication & User Management
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    
    # User Profile & Settings
    path('user/', account_view, name='user'),
    path('settings/', account_settings_view, name='settings'),
    path('profile/<str:mc_username>/', PublicProfileView.as_view(), name='public_profile'),
    
    # Order Management
    path('order/management', OrderManagerView.as_view(), name='order_manager'),
    path('order/<int:pk>/edit/', OrderCardUpdateView.as_view(), name='order_card_edit'),
    path('order/<int:pk>/delete/', OrderCardDeleteView.as_view(), name='order_card_delete'),
    
    # Social Features
    path('', include("app_social.urls")),
]
