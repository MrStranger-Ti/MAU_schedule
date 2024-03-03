from django.urls import path

from profiles.views import ProfileView, ProfileUpdateView

app_name = 'profiles'


urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update', ProfileUpdateView.as_view(), name='profile_update'),
]
