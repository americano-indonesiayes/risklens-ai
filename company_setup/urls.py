from django.urls import path
from .views import show_company

urlpatterns = [
    path("", show_company, name="company_setup"),
]
