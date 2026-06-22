from django.db import models

class AttributionWindow(models.TextChoices):
    """
    Marketing temporality of the extracted data.

    day0  -> Extracted the morning after the performance date.
    day7  -> Extracted 7 days after the performance date.
    day30 -> Extracted 30 days after the performance date.
    """
    DAY0 = "day0", "Day 0"
    DAY7 = "day7", "Day 7"
    DAY30 = "day30", "Day 30"

class FileIngestion(models.Model):
    """
    Metadata describing a CSV file ingestion.

    This table stores ingestion-level information only.
    Actual AppLovin performance rows are stored separately in the raw data tables.

    The purpose of this model is to provide lineage, replayability, and ingestion auditability.
    """
    filename = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, unique=True)    # keep a track of ingested files
    extraction_date = models.DateField()                        # the day the API is called
    attribution_window = models.CharField(
        max_length=10,
        choices=AttributionWindow.choices,
    )
    row_count = models.PositiveIntegerField(default=0)
    ingested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename