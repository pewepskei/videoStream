from celery import shared_task
from .models import Video, Category
from django.contrib.auth.models import User

@shared_task
def uploadVideoFiles(form_data):
    titles = form_data['titles']
    descriptions = form_data['descriptions']
    video_files = form_data['video_files']
    thumbnails = form_data['thumbnails']
    categories = form_data['categories']
    uploader = form_data['uploader_id']

    # Iterate through the data lists and save each Video instance
    for i in range(len(titles)):
        video_instance = Video(
            title=titles[i],
            description=descriptions[i],
            video_file=video_files[i],
            thumbnail=thumbnails[i],
            category=Category.objects.get(id=categories[i]),
            uploader=User.objects.get(id=uploader)
        )
        video_instance.save()
