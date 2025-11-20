from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Place, Image


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


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["place", "image", "image_preview"]
    list_filter = ["place"]
    search_fields = ["place__title"]
    readonly_fields = ["image_preview"]
    fields = ["place", "image", "image_preview", "position"]
