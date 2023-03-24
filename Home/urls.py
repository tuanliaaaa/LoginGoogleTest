
from django.urls import path
from .views import LoginByGoogle
urlpatterns = [
    path('Login',LoginByGoogle.as_view() ),
]
