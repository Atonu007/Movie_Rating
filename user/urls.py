from django.urls import path
from .views import UserRegistration


urlpatterns = [
    path('user-registration/',UserRegistration.as_view(), name='user-registration')
]