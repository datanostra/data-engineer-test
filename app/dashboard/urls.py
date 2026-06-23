from django.urls import path

from app.dashboard.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]