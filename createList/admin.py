from django.contrib import admin

# Register your models here.

from .models import List, Thing, MatchUp


class ListAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name")}
  

admin.site.register(List)
admin.site.register(Thing)
admin.site.register(MatchUp)
