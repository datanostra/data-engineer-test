from django.urls import path
from app.api.views import campaigns, ads

urlpatterns = [
    path("campaigns", campaigns),
    path("ads", ads),
]