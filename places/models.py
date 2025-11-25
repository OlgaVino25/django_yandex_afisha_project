from django.db import models
from django.utils.html import format_html


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    long_description = models.TextField(verbose_name="Полное описание", blank=True)
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="images", verbose_name="Место"
    )
    image = models.ImageField(upload_to="places/", verbose_name="Изображение")
    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция",
        help_text="Чем меньше число, тем выше в списке",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["position"]
        indexes = [
            models.Index(fields=["position"]),
        ]

    def __str__(self):
        return f"Изображение {self.position} для {self.place.title}"

    def image_preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;"/>', self.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"
