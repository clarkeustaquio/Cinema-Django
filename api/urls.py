from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('movies/', views.movie_api, name="movie_api"),
    path('title=<slug>/', views.movie_api_slug, name='movie_api_slug'),
    path('search_movie/', views.search_movie, name='search_movie'),
]