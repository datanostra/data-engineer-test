from django.core.management.base import BaseCommand

from app.models import FileIngestion, RawAdsRow

class Command(BaseCommand):
    help = "Delete all ingested data."

    def handle(self, *args, **options):

        raw_rows_deleted, _ = RawAdsRow.objects.all().delete()

        ingestions_deleted, _ = FileIngestion.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {raw_rows_deleted} raw rows and "
                f"{ingestions_deleted} ingestions."
            )
        )