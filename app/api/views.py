from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.api.selectors import get_campaign_kpis, get_ad_kpis


@api_view(["GET"])
def campaigns(request):
    """
    Return campaign-level performance metrics.

    The endpoint exposes aggregated KPIs computed from the curated
    dataset for a given attribution window. Optional query parameters
    can be used to filter the dataset before aggregation.

    Supported filters:
    - attribution_window
    - date_from
    - date_to
    - platform
    - country
    - country_x_language
    - campaign_name
    """
    data = list(get_campaign_kpis(request.query_params))
    return Response(data)


@api_view(["GET"])
def ads(request):
    """
    Return ad-level performance metrics.

    The endpoint exposes aggregated KPIs computed from the curated
    dataset at the ad granularity. Optional query parameters can be
    used to restrict the dataset before KPI calculation.

    Supported filters:
    - attribution_window
    - date_from
    - date_to
    - platform
    - country
    - country_x_language
    - campaign_name
    - ad_name
    """
    data = list(get_ad_kpis(request.query_params))
    return Response(data)