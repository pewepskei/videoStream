from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator as FEV

video_path = "uploads/video_files"
thumb_path = "uploads/thumb_files"
video_extensions = ["mp4"]
thumb_extensions = ["png", "jpg", "jpeg"]
# Create your models here.
class Video(models.Model):
    Title       = models.CharField(max_length=20)
    Description = models.TextField()
    Video_file  = models.FileField(upload_to=video_path, 
                                validators = [FEV(allowed_extensions=video_extensions)])
    Thumbnail   = models.FileField(upload_to=thumb_path, 
                                validators = [FEV(allowed_extensions=thumb_extensions)])
    Date_posted = models.DateTimeField(default=timezone.now)