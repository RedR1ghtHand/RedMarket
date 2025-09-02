from django.urls import path

from .views import MessageRedirectView, ReputationHandlerView, ThreadDetailView

urlpatterns = [
    path("messages/", ThreadDetailView.as_view(), name="thread_detail"),
    path("messages/<int:thread_id>/", ThreadDetailView.as_view(), name="thread_detail"),
    path('message/<str:mc_username>/', MessageRedirectView.as_view(), name='start_message'),
    path('reputation/<str:mc_username>/', ReputationHandlerView.as_view(), name='profile_reputation'),
]
