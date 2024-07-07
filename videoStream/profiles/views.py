from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Profile
from main.models import Video

# Create your views here.
class profileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        video = Video.objects.all().filter(uploader=pk).order_by('-date_posted')
        # video = Video.objects.all().order_by('-date_posted')
        print(pk)

        context = {
            'profile': profile,
            'videos': video
        }
        print(profile)
        print(video)

        return render(request, 'profiles/profile.html', context)
    
class updateProfile(UpdateView):
    model = Profile
    fields = ['name', 'bio', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.jpg'
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.object.pk})