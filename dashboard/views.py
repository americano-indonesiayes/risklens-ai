from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required
from document_analyzer.models import DocumentAnalysis

@login_required(login_url='login')
@role_required("admin")
def show_dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url='login')
@role_required("employee")
def show_dashboard_employee(request):
    qs = DocumentAnalysis.objects.filter(user=request.user)
    total_count = qs.count()
    safe_count = qs.filter(risk_level=DocumentAnalysis.RiskLevel.SAFE).count()
    moderate_count = qs.filter(risk_level=DocumentAnalysis.RiskLevel.MODERATE).count()
    high_count = qs.filter(risk_level=DocumentAnalysis.RiskLevel.HIGH).count()

    recent_analyses = qs.order_by("-created_at")[:6]

    if total_count:
        safe_pct = round((safe_count / total_count) * 100)
        moderate_pct = round((moderate_count / total_count) * 100)
        high_pct = max(0, 100 - safe_pct - moderate_pct)
    else:
        safe_pct = moderate_pct = high_pct = 0
    high_moderate_pct = high_pct + moderate_pct

    risk_distribution = {
        "safe": safe_count,
        "moderate": moderate_count,
        "high": high_count,
        "total": total_count,
        "safe_pct": safe_pct,
        "moderate_pct": moderate_pct,
        "high_pct": high_pct,
        "high_moderate_pct": high_moderate_pct,
    }

    context = {
        "total_count": total_count,
        "safe_count": safe_count,
        "moderate_count": moderate_count,
        "high_count": high_count,
        "recent_analyses": recent_analyses,
        "risk_distribution": risk_distribution,
    }
    return render(request, "dashboard_employee.html", context)
