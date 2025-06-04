from django.db import models
from django.utils import timezone


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=100, unique=True) #Note uniqueness
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    # ^ Must call model.save() when any element of List is updated
    
    
    #on delete, cascade


class Thing(models.Model):
    name = models.CharField(max_length=1000)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # Image
    # Match History

class MatchUp(models.Model):
    winner = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_won')
    loser = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_lost')
    
# User/List owner field?
