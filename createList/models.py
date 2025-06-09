from django.db import models
from django.utils import timezone


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=100, unique=True) #Note uniqueness
    image = models.ImageField(upload_to='media/list_images')
    description = models.CharField(max_length=1000)
    
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    # ^ Must call model.save() when any element of List is updated
    slug = models.SlugField(default="", null=False, unique=True)

class Thing(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='media/thing_images')
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # Match History

class MatchUp(models.Model):
    winner = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_won')
    loser = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_lost')
    
# User/List owner field?



from django.db.models import Q

serialnumber_is_not_blank = ~Q(serial_number="")

class Meta:
   constraints = [
        models.UniqueConstraint(
            fields=["serial_number"],
            condition=serialnumber_is_not_blank,
            name="unique_serial_number",
        )
    ]
