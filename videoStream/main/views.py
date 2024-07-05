from django.shortcuts import render, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Video

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

class uploadVideo(CreateView):
    model  = Video
    fields = ['Title', 'Description', 'Video_file', 'Thumbnail']
    template_name = 'main/uploadVid.html'

    def get_success_url(self) -> str:
        return reverse('play-video', kwargs={'pk': self.object.pk})
    
class viewVideo(DetailView):
    model = Video
    template_name = 'main/playVid.html'

class updateVideo(UpdateView):
    model = Video
    fields = ['Title', 'Description', 'Thumbnail']
    template_name = 'main/uploadVid.html'

    def get_success_url(self) -> str:
        return reverse('play-video', kwargs={'pk': self.object.pk})
    
class deleteVideo(DeleteView):
    model = Video
    template_name = 'main/deleteVid.html'
    
    def get_success_url(self) -> str:
        return reverse('home')