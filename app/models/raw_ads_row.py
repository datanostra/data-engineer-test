from django.db import models

from .file_ingestion import FileIngestion

class RawAdsRow(models.Model):
    """
    Original raw AppLovin performance row as received from the source file.

    This table is append-only and can grow quickly because every ingested
    version of a business row is preserved. It is not intended to serve
    high-frequency analytical queries directly.

    For production-scale workloads, this layer would typically be stored in
    S3 as immutable partitioned files, with query access through Athena/Glue
    or a lakehouse table format. The local implementation keeps it in the
    database for simplicity and testability.
    """
    ingestion = models.ForeignKey(
        FileIngestion,
        on_delete=models.CASCADE,
        related_name="rows",
    )

    date = models.DateField(
        help_text="Performance date."
    )

    platform = models.CharField(
        max_length=20,
        help_text="Platform (ios or android)."
    )

    country_x_language = models.CharField(
        max_length=20,
        help_text="Country and language combination."
    )

    campaign_id = models.CharField(
        max_length=255,
        help_text="Campaign identifier."
    )

    ad_id = models.CharField(
        max_length=255,
        help_text="Ad identifier."
    )

    spend = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        help_text="Advertising spend."
    )

    installs = models.IntegerField(
        help_text="Number of installs."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.date} | "
            f"{self.campaign_id} | "
            f"{self.ad_id}"
        )