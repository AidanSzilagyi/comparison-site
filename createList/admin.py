from django.contrib import admin

# Register your models here.

from .models import List, Thing, Matchup, Profile, SeenThing


class ListAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name")}
  
admin.site.register(Profile)
admin.site.register(List)
admin.site.register(Thing)
admin.site.register(Matchup)
admin.site.register(SeenThing)
