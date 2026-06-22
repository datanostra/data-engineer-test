from django.core.management.base import BaseCommand

from app.services.ingestion import ingest_directory

class Command(BaseCommand):
    help = "Ingest all CSV files from a directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="data/source",
            help="Directory containing AppLovin CSV files.",
        )

    def handle(self, *args, **options):
        directory_path = options["path"]

        self.stdout.write(f"Starting directory ingestion: {directory_path}")

        result = ingest_directory(directory_path)

        self.stdout.write(
            self.style.SUCCESS(
                f"Directory ingestion completed. "
                f"Files: {result['files_count']}, "
                f"Ingested: {result['ingested_count']}, "
                f"Skipped: {result['skipped_count']}"
            )
        )