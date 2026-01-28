from django.urls import path
from .views import show_dashboard

urlpatterns = [
    path("", show_dashboard, name="dashboard"),
]
