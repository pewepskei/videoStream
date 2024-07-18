from django import forms
from .models import Video

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

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'category']  # Specify the fields from the model

    # Custom multiple file field
    #files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    vidoe_files = MultipleFileField()
    thumbnail = MultipleFileField()

#    def clean_files(self):
#        files = self.cleaned_data.get('files')
#        if files:
#            if len(files) > 5:
#                raise forms.ValidationError('You cannot upload more than 5 files.')
#        return files

    def is_valid(self):
        # Custom validation logic
        valid = super().is_valid()  # Run the parent class validation
        #valid = True  # Run the parent class validation
        if valid:
            # Perforddum additional validation chiecks
            print("Passed initial validation")
        else:
            print("Sadly failed main validation")
        
        #return False
        return valid

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Handle saving of files here if needed
        if commit:
            instance.save()
        return instance
