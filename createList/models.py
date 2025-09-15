from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.postgres.fields import CICharField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True, validators=[RegexValidator(regex=r'^[a-zA-z0-9_-]+$')])
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    class Meta:
        constraints = [
            UniqueConstraint(Lower("username"), name="unique_lower_username")
        ]

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_profile_slug(self)
        super().save(*args, **kwargs)

class List(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='list_images/', blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    # ^ Must call list.save() when any element of List is updated
    
    class Permission(models.TextChoices):
        PRIVATE = 'private', 'Private'
        PROTECTED = 'protected', 'View Only'
        INVITE_RANK = 'invite-rank', 'Invite to Rank'
        INVITE_VIEW = 'invite-view', 'Invite to View'
        PUBLIC = 'public', 'Public'
        
        @property
        def requires_invite(self):
            return self in {self.INVITE_RANK, self.INVITE_VIEW}

    permission_descriptions = {
        Permission.PRIVATE: "Only you can view and rank this list.",
        Permission.PROTECTED: "Anyone with the link can view, but not rank.",
        Permission.INVITE_RANK: "Only invited users can rank. Others can view.",
        Permission.INVITE_VIEW: "Only invited users can view and rank.",
        Permission.PUBLIC: "Anyone can view and rank this list.",
    }

    permission = models.CharField(
        max_length=20,
        choices=Permission.choices,
        default=Permission.PRIVATE,
        help_text="Controls who can view or rank this list."
    )
    # permitted_users field only used with invite-related permissions, but is always there.
    permitted_users = models.ManyToManyField(User, related_name="permitted_lists")
    
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_list_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Thing(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default="") #default is for blank forms, not for actual storage
    image = models.ImageField(upload_to='thing_images/', blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    rating = models.DecimalField(default=0.0, max_digits=7, decimal_places=4)
    times_compared = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} --- {self.rating}"

class Matchup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    winner = models.ForeignKey(Thing, null=True, on_delete=models.CASCADE, related_name='matchups_won')
    loser = models.ForeignKey(Thing, null=True, on_delete=models.CASCADE, related_name='matchups_lost')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    awaiting_response = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.winner.name} vs {self.loser.name}"
    
# If the winner is deleted, make sure to decrement number of losses
# for the loser before the Matchup is deleted.
@receiver(pre_delete, sender=Matchup)
def adjust_stats_on_matchup_delete(sender, instance, **kwargs):
    if instance.winner_id:
        instance.winner.wins = models.F("wins") - 1
        instance.winner.times_compared = models.F("times_compared") - 1
        instance.winner.save(update_fields=["wins", "times_compared"])
    if instance.loser_id:
        instance.loser.losses = models.F("losses") - 1
        instance.loser.times_compared = models.F("times_compared") - 1
        instance.loser.save(update_fields=["losses", "times_compared"])
    
        
class RecentListInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    interaction_time = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'list')
        ordering = ['-interaction_time']

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
        
    
    