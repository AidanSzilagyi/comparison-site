from django.db import models
from django.utils import timezone


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) #Note uniqueness
    image = models.ImageField(upload_to='media/list_images', blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    # ^ Must call model.save() when any element of List is updated
    slug = models.SlugField(blank=True, null=True, unique=True)
    def __str__(self):
        return self.name

class Thing(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='media/thing_images', blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # Match History
    def __str__(self):
        return self.name

class MatchUp(models.Model):
    winner = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_won')
    loser = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_lost')
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.winner} vs {self.loser}"
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
