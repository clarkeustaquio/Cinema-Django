from rest_framework import serializers
from cinema_core.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_title', 'movie_description', 'movie_length', 'movie_link',]
        # Have to include ratings, cast(actors and actress), genre of the movie(horror and etc)