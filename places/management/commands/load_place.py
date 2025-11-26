import json
import os

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned

from places.models import Image, Place


class Command(BaseCommand):
    help = "Загружать данные о месте из файла JSON или URL-адреса"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="Path or URL to JSON file")

    def handle(self, *args, **options):
        source = options["source"]

        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            payload = response.json()
        else:
            with open(source, "r", encoding="utf-8") as f:
                payload = json.load(f)

        title = payload["title"]
        short_description = payload["description_short"]
        long_description = payload["description_long"]
        lng = float(payload["coordinates"]["lng"])
        lat = float(payload["coordinates"]["lat"])
        imgs = payload["imgs"]

        try:
            place, created = Place.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": short_description,
                    "long_description": long_description,
                    "lng": lng,
                    "lat": lat,
                },
            )
        except MultipleObjectsReturned:
            self.stderr.write(
                self.style.ERROR(
                    f"Found multiple places with title '{title}'. "
                    "Please resolve duplicates manually."
                )
            )
            return

        self.stdout.write(f"{'Created' if created else 'Updated'} place: {title}")

        place.images.all().delete()

        for position, img_url in enumerate(payload["imgs"]):
            filename = img_url.split("/")[-1]

            try:
                if img_url.startswith("http"):
                    response = requests.get(img_url)
                    response.raise_for_status()
                    content = response.content
                    self.stdout.write(f"Downloaded image: {filename}")
                else:
                    with open(img_url, "rb") as f:
                        content = f.read()
                    self.stdout.write(f"Used local image: {filename}")

                Image.objects.create(
                    place=place,
                    position=position,
                    image=ContentFile(content, name=filename),
                )

            except (requests.RequestException, IOError) as e:
                self.stderr.write(f"Failed to load {img_url}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded place: {title}"))
