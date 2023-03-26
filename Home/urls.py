
from django.urls import path
from .views import LoginByGoogle,LoginGoogleResponse,Home
urlpatterns = [
    path('Login',LoginByGoogle.as_view() ),
    path('LoginGoogleResponse',LoginGoogleResponse.as_view(),name='oauth2callback' ),
    path('home',Home.as_view(),name='home' ),
]

