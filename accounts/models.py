from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.CharField(max_length=150)
    theater = models.CharField(max_length=100)
    price = models.IntegerField()
    seat = models.CharField(max_length=50)
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=150)

    def __str__(self):
        return "{} - {}".format(self.user, self.movie)