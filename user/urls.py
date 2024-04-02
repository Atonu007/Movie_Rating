from django.urls import path
from .views import UserRegistration,UserLogin,AddMovieAPIView


urlpatterns = [
    path('user-registration/',UserRegistration.as_view(), name='user-registration'),
    path('user-login/',UserLogin.as_view(), name='user-login'),
    path('add-movie/',AddMovieAPIView.as_view(), name='add-movie')
]