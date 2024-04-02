from django.urls import path
from .views import UserRegistration,UserLogin


urlpatterns = [
    path('user-registration/',UserRegistration.as_view(), name='user-registration'),
    path('user-login/',UserLogin.as_view(), name='user-login')
]