from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Profile
from main.models import Video

# Create your views here.
class profileView(View):
    def get(self, request,  *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        video = Video.objects.all().filter(uploader=request.user).order_by('-date_posted')

        context = {
            'profile': profile,
            'videos': video
        }

        return render(request, 'profiles/profile.html', context)
    
class updateProfile(UpdateView):
    model = Profile
    fields = ['name', 'bio', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.jpg'
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        # Override get_object to fetch Profile based on username
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self) -> str:
        user = self.kwargs.get('user')
        return reverse('profile', kwargs={'user': user})