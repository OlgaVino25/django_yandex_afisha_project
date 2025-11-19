from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["title", "lng", "lat"]
    search_fields = ["title"]
    list_display_links = ["title"]
