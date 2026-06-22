from django.core.management.base import BaseCommand

from app.services.ingestion import ingest_file

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):

        file_path = options["file_path"]
        
        self.stdout.write(f"Starting ingestion: {file_path}")

        result = ingest_file(file_path)

        if result["status"] == "skipped":
            self.stdout.write(
                self.style.WARNING(
                    f"Skipped: {result['filename']} was already ingested."
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested {result['row_count']} rows "
                f"from {result['filename']}"
            )
        )