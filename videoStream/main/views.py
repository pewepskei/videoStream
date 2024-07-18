from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Video, Comments
from .forms import CommentForm, VideoForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class home(ListView):
    model = Video
    template_name = "main/home.html"
    order_by = '-date_posted'

class uploadVideo(LoginRequiredMixin, CreateView):
    print("Now inside uploadVideo")
    model  = Video
    form_class = VideoForm
    #fields = ['title', 'description', 'video_file', 'thumbnail','category']
    template_name = 'main/uploadVid.html'
    success_url = reverse_lazy('play-video')

    def post(self, request, *args, **kwargs):
        print("Received POST Method")
        print(request.POST)
        print(request.FILES)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Checking if form is valid")
        form.instance.uploader = self.request.user
        print(f"Form uploader: {form.instance.uploader}")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid Form")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        print("Running get_success_url")
        return reverse('play-video', kwargs={'pk': self.object.pk})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        print("received POST Method")
        files = request.FILES.getlist('file')
        for file in files:
            print(f"Files are: {file}")

    else:
        form = VideoForm
    return render (request, 'main/addVideo.html', {'form': form})

class viewVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm()
        comments = Comments.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]
        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories
        }
        return render(request, 'main/playVid.html', context)

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            user = str(self.request.user)
            response = {
                'user'    : user,
                'comment' : form.cleaned_data['comment'],
            }
            comment = Comments(
                user = self.request.user,
                comment = form.cleaned_data['comment'],
                video = video
            )
            comment.save()
        
        comments = Comments.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]
        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories
        }
        return JsonResponse(response)

class updateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'thumbnail']
    template_name = 'main/uploadVid.html'

    def get_success_url(self) -> str:
        return reverse('play-video', kwargs={'pk': self.object.pk})
    
    def test_func(self) -> bool | None:
        video = self.get_object()
        return self.request.user == video.uploader
    
class deleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'main/deleteVid.html'
    
    def get_success_url(self) -> str:
        return reverse('home')
    
    def test_func(self) -> bool | None:
        video = self.get_object()
        return self.request.user == video.uploader
    
class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        query_list = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploader__username__icontains=query)
        )
        context = {
            "query_list": query_list
        }
        return render(request, 'main/search.html', context)
