from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('history/', views.history, name='history'),
]