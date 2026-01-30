from django.contrib import admin
from .models import DocumentAnalysis


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "risk_level", "status", "created_at")
    list_filter = ("risk_level", "status", "created_at")
    search_fields = ("user__username", "input_preview")

# Register your models here.
