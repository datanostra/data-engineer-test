from django.core.management.base import BaseCommand

from app.models import FileIngestion, RawAdsRow, CuratedDay0, CuratedDay7, CuratedDay30

class Command(BaseCommand):
    help = "Delete all ingested data."

    def handle(self, *args, **options):

        curated_day0_deleted, _ = CuratedDay0.objects.all().delete() 
        curated_day7_deleted, _ = CuratedDay7.objects.all().delete() 
        curated_day30_deleted, _ = CuratedDay30.objects.all().delete()
        raw_rows_deleted, _ = RawAdsRow.objects.all().delete()
        ingestions_deleted, _ = FileIngestion.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {raw_rows_deleted} raw rows, "
                f"{ingestions_deleted} ingestions, "
                f"{curated_day0_deleted} curated Day0, "
                f"{curated_day7_deleted} curated Day7, "
                f"{curated_day30_deleted} curated Day30, "
            )
        )