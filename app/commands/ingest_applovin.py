from django.core.management.base import BaseCommand

from app.services.ingestion import ingest_file

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        ingest_file(options["file_path"])

        self.stdout.write(
            self.style.SUCCESS("Ingestion completed.")
        )