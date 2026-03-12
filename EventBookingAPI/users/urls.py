from django.urls import path
from . import views

urlpatterns=[
    path('auth/register/',views.RegistrationView.as_view()),
    path('profile/',views.ProfileView.as_view()),
    path('me/',views.UserView.as_view()),
]
