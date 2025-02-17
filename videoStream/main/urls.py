from django.urls import path
from .views import uploadVideo, viewVideo, updateVideo, deleteVideo, home, SearchVideo

urlpatterns = [
    path('', home.as_view(), name="home"),
    path('upload/', uploadVideo.as_view(), name="upload-video"),
    path('<int:pk>/', viewVideo.as_view(), name="play-video"),
    path('<int:pk>/update', updateVideo.as_view(), name='update-video' ),
    path('<int:pk>/delete', deleteVideo.as_view(), name='delete-video' ),
    path('search/', SearchVideo.as_view(), name='search-video')
]
