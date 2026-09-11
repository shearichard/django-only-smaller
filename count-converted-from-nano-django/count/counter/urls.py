from django.urls import path

from . import views
from .api import api

urlpatterns = [
    path("api/", api.urls),
    path("", views.count, name="count"),
    path("slow/", views.slow, name="slow"),
]
