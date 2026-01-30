from django.urls import path
from .views import show_document

urlpatterns = [
    path("", show_document, name="document_analyzer"),
]
