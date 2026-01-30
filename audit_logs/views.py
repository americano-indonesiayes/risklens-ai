from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required
from document_analyzer.models import DocumentAnalysis

@login_required(login_url='login')
@role_required("employee")
def show_audit(request):
    qs = DocumentAnalysis.objects.filter(user=request.user).order_by("-created_at")

    search_query = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip().upper()
    category_filter = request.GET.get("category", "").strip().upper()

    if search_query:
        qs = qs.filter(input_preview__icontains=search_query)

    if status_filter in DocumentAnalysis.RiskLevel.values:
        qs = qs.filter(risk_level=status_filter)

    if category_filter in DocumentAnalysis.Category.values:
        qs = qs.filter(categories__contains=[category_filter])

    context = {
        "analyses": qs[:100],
        "search_query": search_query,
        "status_filter": status_filter,
        "category_filter": category_filter,
        "risk_levels": DocumentAnalysis.RiskLevel.values,
        "category_options": DocumentAnalysis.Category.values,
    }
    return render(request, "audit.html", context)
