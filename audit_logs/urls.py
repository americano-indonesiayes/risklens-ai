from django.urls import path
from .views import show_audit

urlpatterns = [
    path("", show_audit, name="audit_logs"),
]