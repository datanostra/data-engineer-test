from app.models import CuratedDay0, CuratedDay7, CuratedDay30

CURATED_MODEL_BY_WINDOW = {
    "day0": CuratedDay0,
    "day7": CuratedDay7,
    "day30": CuratedDay30,
}

def get_curated_model(attribution_window: str):
    try:
        return CURATED_MODEL_BY_WINDOW[attribution_window]
    except KeyError:
        raise ValueError(f"Unsupported attribution window: {attribution_window}")


def upsert_curated_rows(raw_rows, attribution_window: str) -> int:
    model = get_curated_model(attribution_window)

    latest_by_key = {}

    for raw_row in raw_rows:
        key = (
            raw_row.date,
            raw_row.platform,
            raw_row.country_x_language,
            raw_row.campaign_id,
            raw_row.ad_id,
        )

        current = latest_by_key.get(key)

        if current is None or raw_row.extraction_date >= current.extraction_date:
            latest_by_key[key] = raw_row

    raw_rows = list(latest_by_key.values())

    changed_count = 0


    for raw_row in raw_rows:
        obj, created = model.objects.update_or_create(
            date=raw_row.date,
            platform=raw_row.platform,
            country_x_language=raw_row.country_x_language,
            campaign_id=raw_row.campaign_id,
            ad_id=raw_row.ad_id,
            defaults={
                "country": raw_row.country,
                "media": raw_row.media,
                "campaign_name": raw_row.campaign_name,
                "ad_name": raw_row.ad_name,
                "short_ad_name": raw_row.short_ad_name,
                "ad_type": raw_row.ad_type,
                "ad_creative_type": raw_row.ad_creative_type,
                "spend": raw_row.spend,
                "impressions": raw_row.impressions,
                "clicks": raw_row.clicks,
                "installs": raw_row.installs,
                "sales": raw_row.sales,
                "purchases_d0": raw_row.purchases_d0,
                "purchases_d7": raw_row.purchases_d7,
                "purchases_value_d0": raw_row.purchases_value_d0,
                "purchases_value_d7": raw_row.purchases_value_d7,
                "last_extraction_date": raw_row.extraction_date,
                "last_ingestion": raw_row.ingestion,
                "row_hash": raw_row.row_hash,
            },
        )

        if created:
            changed_count += 1
            continue

        if raw_row.extraction_date >= obj.last_extraction_date:
            for field, value in defaults.items():
                setattr(obj, field, value)

            obj.save()
            changed_count += 1

    return changed_count