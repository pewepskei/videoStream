from celery import shared_task
from .models import Video, Category
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
@shared_task
def uploadVideoFiles(id, video_file, thumbnail):
    video = Video.objects.get(id=id)
    logger.info(f"Uploading video {video.title}")

    video_path = f"server/disk/{video.title}.mp4"
    thumb_path = f"server/disk/{video.title}.png"

    with open(video_path, 'wb') as f:
        f.write(video_file)

    with open(thumb_path, 'wb') as f:
        f.write(thumbnail)

    return "Done Uploading"

