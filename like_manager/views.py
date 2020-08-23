from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from cinema_core.models import Movie
from .models import Like, Dislike
from .serializers import LikeSerializer, DislikeSerializer
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def like(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    _like = Like.objects.filter(user=request.user, movie=movie)
    _dislike = Dislike.objects.filter(user=request.user, movie=movie)

    if _like.exists():
        like = _like.delete()
    elif not _like.exists():
        if _dislike.exists():
            _dislike.delete()
            like = Like.objects.create(user = request.user,movie = movie)
        else:
            like = Like.objects.create(user = request.user,movie = movie)
    return JsonResponse({'slug': slug}, safe=False, json_dumps_params={'indent': 4})
    # serializers = LikeSerializer(like)
    # return JsonResponse(serializers.data, safe=False, json_dumps_params={'indent': 4})
    
@login_required
def dislike(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    _like = Like.objects.filter(user=request.user, movie=movie)
    _dislike = Dislike.objects.filter(user=request.user, movie=movie)

    if _dislike.exists():
        dislike = _dislike.delete()
    elif not _dislike.exists():
        if _like.exists():
            _like.delete()
            dislike = Dislike.objects.create(user = request.user,movie = movie)
        else:
            dislike = Dislike.objects.create(user = request.user,movie = movie)

    serializers = DislikeSerializer(dislike)
    return JsonResponse(serializers.data, safe=False, json_dumps_params={'indent': 4})