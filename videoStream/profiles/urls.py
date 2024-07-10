from django.urls import path
from .views import profileView, updateProfile

urlpatterns = [
    path('<str:user>/', profileView.as_view(), name="profile"),
    path('<str:user>/update', updateProfile.as_view(), name="update-profile"),
]
