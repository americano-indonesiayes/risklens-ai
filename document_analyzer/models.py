from django.db import models
from django.contrib.auth.models import User


class DocumentAnalysis(models.Model):
    class RiskLevel(models.TextChoices):
        SAFE = "SAFE", "Safe"
        MODERATE = "MODERATE", "Moderate"
        HIGH = "HIGH", "High"

    class Disclosure(models.TextChoices):
        PUBLIC_SAFE = "PUBLIC_SAFE", "Public Safe"
        INTERNAL_ONLY = "INTERNAL_ONLY", "Internal Only"
        RESTRICTED = "RESTRICTED", "Restricted"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    class Category(models.TextChoices):
        PII = "PII", "Personal Identifiable Info"
        SECRETS = "SECRETS", "Secrets"
        SOCIAL_ENGINEERING = "SOCIAL_ENGINEERING", "Social Engineering"
        CONFIDENTIAL_BUSINESS = "CONFIDENTIAL_BUSINESS", "Confidential Business"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="document_analyses")
    created_at = models.DateTimeField(auto_now_add=True)
    input_text = models.TextField()
    input_preview = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=16, choices=RiskLevel.choices, default=RiskLevel.SAFE)
    recommended_disclosure = models.CharField(
        max_length=32,
        choices=Disclosure.choices,
        default=Disclosure.INTERNAL_ONLY,
    )
    flag_reasons = models.JSONField(default=list, blank=True)
    categories = models.JSONField(default=list, blank=True)
    safe_version = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.user.username} - {self.risk_level} - {self.created_at:%Y-%m-%d %H:%M}"
