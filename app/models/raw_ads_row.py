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

    extraction_date = models.DateField()
    attribution_window = models.CharField(max_length=10)

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

    country = models.CharField(max_length=2)
    media = models.CharField(max_length=100)

    campaign_name = models.TextField()
    ad_name = models.TextField()
    short_ad_name = models.TextField(blank=True, null=True)
    ad_type = models.CharField(max_length=100, blank=True, null=True)
    ad_creative_type = models.CharField(max_length=100, blank=True, null=True)

    impressions = models.BigIntegerField()
    clicks = models.BigIntegerField()
    sales = models.BigIntegerField()

    purchases_d0 = models.BigIntegerField()
    purchases_d7 = models.BigIntegerField()

    purchases_value_d0 = models.DecimalField(max_digits=18, decimal_places=6)
    purchases_value_d7 = models.DecimalField(max_digits=18, decimal_places=6)

    row_hash = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["attribution_window", "extraction_date"]),
            models.Index(fields=["date", "platform"]),
            models.Index(fields=["campaign_id", "ad_id"]),
        ]

    def __str__(self):
        return (
            f"{self.date} | "
            f"{self.campaign_id} | "
            f"{self.ad_id}"
        )