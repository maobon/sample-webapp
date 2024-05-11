
from django.urls import path,include

from . import views

app_name = 'users'
urlpatterns = [
    # login logout
    path('', include('django.contrib.auth.urls')),
    # register
    path('register/', views.register, name='register'),
]