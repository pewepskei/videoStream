from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator as FEV
from django.contrib.auth.models import User

video_path = "uploads/video_files"
thumb_path = "uploads/thumb_files"
video_extensions = ["mp4"]
thumb_extensions = ["png", "jpg", "jpeg"]
# Create your models here.
class Video(models.Model):
    uploader    = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    description = models.TextField()
    video_file  = models.FileField(upload_to=video_path, 
                                validators = [FEV(allowed_extensions=video_extensions)])
    thumbnail   = models.FileField(upload_to=thumb_path, 
                                validators = [FEV(allowed_extensions=thumb_extensions)])
    date_posted = models.DateTimeField(default=timezone.now)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} | {self.created_on.strftime('%b %d %Y %I:%M %p')}"