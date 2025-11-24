import glob

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загрузка всех файлов JSON в каталоге static/places"

    def handle(self, *args, **options):
        json_files = glob.glob("static/places/*.json")

        if not json_files:
            self.stdout.write(
                self.style.WARNING("No JSON files found in static/places/")
            )
            return

        self.stdout.write(f"Found {len(json_files)} JSON files")

        for json_file in json_files:
            try:
                self.stdout.write(f"Loading {json_file}...")
                call_command("load_place", json_file)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded {json_file}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error loading {json_file}: {str(e)}")
                )

        self.stdout.write(self.style.SUCCESS("Finished loading all places"))
