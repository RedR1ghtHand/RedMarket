from django.urls import path
from .views import MessageRedirectView, ThreadDetailView

urlpatterns = [
    path("messages/", ThreadDetailView.as_view(), name="thread_detail"),
    path("messages/<int:thread_id>/", ThreadDetailView.as_view(), name="thread_detail"),
    path('message/<str:mc_username>/', MessageRedirectView.as_view(), name='start_message')
]
