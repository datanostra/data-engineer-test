from django.db.models import Sum, Value, FloatField, F, ExpressionWrapper
from django.db.models.functions import Coalesce

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
        raise ValueError(f"Invalid attribution_window: {attribution_window}")


def apply_filters(queryset, params):
    """
    Apply optional API filters to a queryset.

    Filters are dynamically derived from query parameters and only
    applied when provided by the client. This allows the same
    filtering logic to be reused across campaign and ad endpoints.
    """
    date_from = params.get("date_from")
    date_to = params.get("date_to")

    if date_from:
        queryset = queryset.filter(date__gte=date_from)

    if date_to:
        queryset = queryset.filter(date__lte=date_to)

    for field in [
        "platform",
        "country",
        "country_x_language",
        "campaign_name",
        "ad_name",
    ]:
        value = params.get(field)
        if value:
            queryset = queryset.filter(**{field: value})

    return queryset


def with_kpis(queryset):

    # Group data by campaign and compute aggregated metrics across all ads
    queryset = queryset.annotate(
        spend=Sum("spend"),
        installs=Sum("installs"),
        purchases_d0=Sum("purchases_d0"),
        purchases_d7=Sum("purchases_d7"),
        purchases_value_d7=Sum("purchases_value_d7"),
    )

    return queryset.annotate(
        cpi=ExpressionWrapper(
            F("spend") / F("installs"),
            output_field=FloatField(),
        ),
        cpa_d7=ExpressionWrapper(
            F("spend") / F("purchases_d7"),
            output_field=FloatField(),
        ),
        roas_d7=ExpressionWrapper(
            F("purchases_value_d7") / F("spend"),
            output_field=FloatField(),
        ),
    )


def get_campaign_kpis(params):
    """
    Retrieve campaign-level KPIs from the curated dataset.

    The requested attribution window determines which curated table
    is queried among day0, day7, or day30 (default is day7). 

    Returns campaign performance metrics enriched with derived KPIs
    such as CPI, CPA, and ROAS.
    """
    attribution_window = params.get("attribution_window", "day7")
    model = get_curated_model(attribution_window)

    queryset = apply_filters(model.objects.all(), params)

    queryset = queryset.values(
        "campaign_id",
        "campaign_name",
    )

    return with_kpis(queryset).order_by("campaign_name")


def get_ad_kpis(params):
    attribution_window = params.get("attribution_window", "day7")
    model = get_curated_model(attribution_window)

    queryset = apply_filters(model.objects.all(), params)

    queryset = queryset.values(
        "campaign_id",
        "campaign_name",
        "ad_id",
        "ad_name",
    )

    return with_kpis(queryset).order_by("campaign_name", "ad_name")