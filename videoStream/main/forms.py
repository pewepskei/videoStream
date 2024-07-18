from django import forms
from .models import Video, Category
from django.db import models

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "form-control",
            "placeholder": "Leave a comment ...",
            "rows": 1   
        }
        ))

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MultipleFileField2(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class VideoForm(forms.ModelForm):
    # video_file = MultipleFileField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'category']  # Specify the fields from the model

    def is_valid(self) -> bool:
        return True