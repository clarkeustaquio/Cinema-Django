from django.db import models
from django.contrib.auth.models import User
from cinema_core.models import Movie

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.movie, self.user)

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.movie, self.user)