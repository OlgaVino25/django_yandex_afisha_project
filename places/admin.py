from django import forms
from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from tinymce.widgets import TinyMCE

from .models import Image, Place


class PlaceAdminForm(forms.ModelForm):
    description_short = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}))
    description_long = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = Place
        fields = "__all__"


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ["image", "image_preview", "position"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        return obj.image_preview()

    image_preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["id", "title", "lng", "lat"]
    search_fields = ["title"]
    list_display_links = ["title"]
    inlines = [ImageInline]
    form = PlaceAdminForm


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["place", "image", "image_preview"]
    list_filter = ["place"]
    search_fields = ["place__title"]
    readonly_fields = ["image_preview"]
    fields = ["place", "image", "image_preview", "position"]
