from django.db import models

from .file_ingestion import FileIngestion

class CuratedAdsBase(models.Model):
    """
    Base model for curated advertising performance rows.

    Curated tables store the latest known value for each business key.
    They are optimized for analytical queries and API consumption.

    This model is abstract: Django will not create a table for it.
    """

    date = models.DateField()
    platform = models.CharField(max_length=20)
    country_x_language = models.CharField(max_length=20)

    campaign_id = models.CharField(max_length=255)
    ad_id = models.CharField(max_length=255)

    spend = models.DecimalField(max_digits=18, decimal_places=6)
    installs = models.IntegerField()

    last_extraction_date = models.DateField()
    last_ingestion = models.ForeignKey(
        FileIngestion,
        on_delete=models.PROTECT,
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

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "date",
                    "platform",
                    "country_x_language",
                    "campaign_id",
                    "ad_id",
                ],
                name="%(class)s_business_key_unique",
            )
        ]

class CuratedDay0(CuratedAdsBase):
    class Meta(CuratedAdsBase.Meta):
        db_table = "curated_day0"

class CuratedDay7(CuratedAdsBase):
    class Meta(CuratedAdsBase.Meta):
        db_table = "curated_day7"

class CuratedDay30(CuratedAdsBase):
    class Meta(CuratedAdsBase.Meta):
        db_table = "curated_day30"