from django.urls import path
from .views import profileView, updateProfile

urlpatterns = [
    path('<int:pk>/', profileView.as_view(), name="profile"),
    path('<int:pk>/update', updateProfile.as_view(), name="update-profile"),
]
