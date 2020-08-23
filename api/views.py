from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from cinema_core.models import Movie
from .serializers import MovieSerializer
from datetime import date, datetime

# Create your views here.
current_date = date.today()
current_time = datetime.utcnow().time()

@api_view(['GET'])
def movie_api(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 4})

@api_view(['GET'])
def movie_api_slug(request, slug):
    if request.method == 'GET':
        try:
            movie=Movie.objects.get(slug=slug)
        except Movie.DoesNotExist:
            response_error = {}
            response_error['detail'] = "Query not found."
            response_error['query'] = "Querying movie: api/title=movie-title/"
            response_error['reminder'] = "Use hypens not spaces."
            return JsonResponse(response_error, json_dumps_params={'indent': 4})
        
        serializers = MovieSerializer(movie)
        return JsonResponse(serializers.data, safe=False, json_dumps_params={'indent': 4})

@api_view(['GET'])
def search_movie(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        title = list()

        for movie in movies:
            if current_date >= movie.start_date and current_date <= movie.end_date:
                title.append(Movie.objects.get(movie_title=movie.movie_title).movie_title)

        return JsonResponse(title, safe=False, json_dumps_params={'indent': 4})