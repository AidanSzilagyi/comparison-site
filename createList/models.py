from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, blank=True, null=True) # REMOVE LATER
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_profile_slug(self)
        super().save(*args, **kwargs)

class List(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=100, blank=True, null=True) #Note uniqueness
    image = models.ImageField(upload_to='list_images/', blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) # REMOVE LATER
    num_things = models.IntegerField(default=0)
    type = models.CharField(
        choices = [
            ('image', 'Images Only'),
            ('text', 'Text and Images'),
        ],
        default='text',
    )
    comparison_method = models.CharField(
        choices= [
            ('bradley_terry', 'Bradley-Terry Model'),
            ('crowd-bt', 'Crowd-BT Model'),
        ],
        default='bradley_terry', max_length=20
    )
    batch_countdown = models.IntegerField(default=0)
    comparisons_made = models.IntegerField(default=0)
    comparisons_needed = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    permission = models.CharField(
        choices = [
            ('private', 'Private'),
            ('protected', 'View Only'),
            ('public', 'Public'),
        ],
        default='private'
    )
    # ^ Must call model.save() when any element of List is updated
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_list_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Thing(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='thing_images/', blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    rating = models.DecimalField(default=0.0, max_digits=7, decimal_places=4)
    times_compared = models.IntegerField(default=0)
    
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    
    # Match History?
    def __str__(self):
        return f"{self.name} --- {self.rating}"

class Matchup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    winner = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_won')
    loser = models.ForeignKey(Thing, null=True, on_delete=models.SET_NULL, related_name='matchups_lost')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    awaiting_response = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.winner.name} vs {self.loser.name}"
class SeenThing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [('user', 'thing')]

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

def generate_profile_slug(profile):
    slug = slugify(profile.username)
    counter = 1
    while Profile.objects.filter(slug=slug).exists():
        slug = slugify(profile.username + "-" + counter)
        counter += 1
    return slug

def generate_list_slug(list):
    slug = slugify(list.name)
    if List.objects.filter(slug=slug).exists():
        slug = slugify(list.name + "-" + list.user.profile.username)
    counter = 1
    while List.objects.filter(slug=slug).exists():
        slug = slugify(list.name + "-" + list.user.profile.username + "-" + counter)
    return slug
        
    
    