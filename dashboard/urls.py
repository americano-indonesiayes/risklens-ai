from django.urls import path
from .views import show_dashboard, show_dashboard_employee

urlpatterns = [
    path("", show_dashboard, name="dashboard"),
    path("employee/", show_dashboard_employee, name="dashboard_employee"),
]
