from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.forms import modelformset_factory
from .models import Video, Comments, Category
from .forms import CommentForm, VideoForm
from .tasks import uploadVideoFiles

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class home(ListView):
    model = Video
    template_name = "main/home.html"
    order_by = '-date_posted'

class uploadVideo(LoginRequiredMixin, CreateView):
    model  = Video
    form_class = VideoForm
    # fields = ['title', 'description', 'video_file', 'thumbnail','category']
    template_name = 'main/uploadVid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create formset with VideoForm
        VideoFormSet = modelformset_factory(Video, form=VideoForm, extra=2)
        context['formset'] = VideoFormSet(queryset=Video.objects.none())
        return context
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.FILES)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        # titles = self.request.POST.getlist('title')
        # descriptions = self.request.POST.getlist('description')
        # video_files = self.request.FILES.getlist('video_file')
        # thumbnails = self.request.FILES.getlist('thumbnail')
        # categories = self.request.POST.getlist('category')

        titles = self.request.POST.getlist('title')
        descriptions = self.request.POST.getlist('description')
        video_files = self.request.FILES.getlist('video_file')
        thumbnails = self.request.FILES.getlist('thumbnail')
        categories = self.request.POST.getlist('category')

        print(titles)
        print(descriptions)
        print(video_files)
        print(thumbnails)
        print(categories)

        # Prepare form data to pass to Celery task
        form_data = {
            'titles': titles,
            'descriptions': descriptions,
            'video_files': [vf.temporary_file_path() for vf in video_files],
            'thumbnails': [tn.temporary_file_path() for tn in thumbnails],
            'categories': categories,
            'uploader_id': self.request.user.id,  # Pass the user ID
        }

        uploadVideoFiles.delay(form_data)

        # for i in range(len(titles) - 1):
        #     video_instance = Video(
        #         title=titles[i],
        #         description=descriptions[i],
        #         video_file=video_files[i],
        #         thumbnail=thumbnails[i],
        #         category=Category.objects.get(id=categories[i]),
        #         uploader=self.request.user
        #     )
        #     video_instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse('play-video', kwargs={'pk': self.object.pk})

class viewVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm()
        comments = Comments.objects.filter(video=video).order_by('-created_on')
        # categories = Video.objects.filter(category=video.category)[:15]
        context = {
            'object': video,
            'comments': comments,
            'form': form,
            # 'categories': categories
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
