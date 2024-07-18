from celery import shared_task
from .models import Video, Category

@shared_task
def uploadVideoFiles(user, post, files):
    titles = post.getlist('title')
    descriptions = post.getlist('description')
    video_files = files.getlist('video_file')
    thumbnails = files.getlist('thumbnail')
    categories = files.getlist('category')

    for i in range(len(titles) - 1):
        video_instance = Video(
            title=titles[i],
            description=descriptions[i],
            video_file=video_files[i],
            thumbnail=thumbnails[i],
            category=Category.objects.get(id=categories[i]),
            uploader=user
        )
        video_instance.save()
