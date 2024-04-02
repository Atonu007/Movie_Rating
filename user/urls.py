from django.urls import path
from .views import MovieListAPIView, MovieSearchAPIView, UserRegistration,UserLogin,AddMovieAPIView,RateMovieAPIView


urlpatterns = [
    path('user-registration/',UserRegistration.as_view(), name='user-registration'),
    path('user-login/',UserLogin.as_view(), name='user-login'),
    path('add-movie/',AddMovieAPIView.as_view(), name='add-movie'),
    path('movies/', MovieListAPIView.as_view(), name='movie_list'),
    path('movies/search/', MovieSearchAPIView.as_view(), name='movie_search'),
    path('movies/<int:movie_id>/rate/', RateMovieAPIView.as_view()),
   
]