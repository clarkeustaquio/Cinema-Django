from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('like/<slug>/', views.like, name='like'),
    path('dislike/<slug>/', views.dislike, name='dislike'),
]