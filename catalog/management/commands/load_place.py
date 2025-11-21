import os
import requests
import json
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Place, Image


class Command(BaseCommand):
    help = "Загружать данные о месте из файла JSON или URL-адреса"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="Path or URL to JSON file")

    def handle(self, *args, **options):
        source = options["source"]

        # Загрузка JSON
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            data = response.json()
        else:
            with open(source, "r", encoding="utf-8") as f:
                data = json.load(f)

        # Извлекаем данные из JSON
        title = data["title"]
        description_short = data["description_short"]
        description_long = data["description_long"]
        lng = float(data["coordinates"]["lng"])
        lat = float(data["coordinates"]["lat"])
        imgs = data["imgs"]

        # Создаем или обновляем место в базе данных
        place, created = Place.objects.get_or_create(
            title=title,
            defaults={
                "description_short": description_short,
                "description_long": description_long,
                "lng": lng,
                "lat": lat,
            },
        )

        if not created:
            place.description_short = description_short
            place.description_long = description_long
            place.lng = lng
            place.lat = lat
            place.save()
            self.stdout.write(f"Updated place: {title}")
        else:
            self.stdout.write(f"Created new place: {title}")

        # Удаляем старые изображения
        place.images.all().delete()

        # Создаем папку для изображений, если её нет
        places_dir = os.path.join(settings.MEDIA_ROOT, "places")
        os.makedirs(places_dir, exist_ok=True)

        for position, img_url in enumerate(imgs):
            filename = img_url.split("/")[-1]
            local_path = os.path.join(places_dir, filename)

            if os.path.exists(local_path):
                with open(local_path, "rb") as f:
                    image = Image(place=place, position=position)
                    image.image.save(filename, ContentFile(f.read()), save=True)
                self.stdout.write(f"Used local image: {filename}")
            else:
                try:
                    response = requests.get(img_url)
                    response.raise_for_status()

                    image = Image(place=place, position=position)
                    image.image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(f"Downloaded image: {filename}")
                except requests.RequestException as e:
                    self.stderr.write(f"Failed to download {img_url}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded place: {title}"))
